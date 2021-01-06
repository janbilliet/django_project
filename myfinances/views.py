from .models import Transaction, Category, Subcategory, Type, Picture
from django.shortcuts import render
from .filters import TransactionsFilter
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm, CategoryForm, SubcategoryForm, TypeForm, PictureForm
from django.shortcuts import render, redirect
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import pandas as pd
import numpy as np
import sqlite3
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import urllib, base64
import json
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.db import connections
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.conf import settings
from IPython.display import HTML


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = PostForm


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm


class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm


def load_categories(request):
    type_id = request.GET.get("type")
    categories = Category.objects.filter(type_id=type_id).order_by("name")
    return render(
        request,
        "myfinances/categories_dropdown_list_options.html",
        {"categories": categories},
    )


def load_subcategories(request):
    category_id = request.GET.get("category")
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by("name")
    return render(
        request,
        "myfinances/subcategories_dropdown_list_options.html",
        {"subcategories": subcategories},
    )


def summary(request):

    finance_list = Transaction.objects.all()
    category_list = Category.objects.all()
    finance_filter = TransactionsFilter(request.GET, queryset=finance_list)
    finance_list = finance_filter.qs

    page = request.GET.get("page", 1)
    paginator = Paginator(finance_list, 100)

    try:
        transacties = paginator.page(page)
    except PageNotAnInteger:
        transacties = paginator.page(1)
    except EmptyPage:
        transacties = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "paginator": paginator,
        "filter": finance_filter,
        "is_paginated": True,
        "transacties": transacties,
        "finance_list": finance_list,
        "category_list": category_list,
    }

    register_matplotlib_converters()  # function unknown
    # Say, 'the default sans-serif font is COMIC SANS'
    plt.rcParams["font.sans-serif"] = "Verdana"
    # Then, 'ALWAYS use sans-serif fonts'
    plt.rcParams["font.family"] = "sans-serif"

    # transform data
    q = finance_list.values()
    p = category_list.values()
    df_transaction = pd.DataFrame.from_records(q)
    df_category = pd.DataFrame.from_records(p)
    df_transaction["date"] = pd.to_datetime(df_transaction["date"])
    df_transaction["date"] = df_transaction["date"].map(lambda dt: dt.replace(day=1))
    df_grouped = df_transaction.groupby(["date"])
    df_result = df_grouped.aggregate(np.sum)
    df_result = df_result.reset_index()
    fig, (ax1) = plt.subplots(
        1, sharex=True, gridspec_kw={"height_ratios": [3]}
    )  # 2 subplots, share x axis, different height size
    fig.set_size_inches(w=11, h=3)
    ax1.bar(
        df_result.date,
        df_result.amount,
        width=np.timedelta64(25, "D"),
        color="lightgrey",
    )
    ax1.xaxis.set_major_formatter(DateFormatter("%Y"))
    ax1.yaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, pos: "{:,.0f}".format(x) + " €")
    )
    ax1.set(xlabel="", ylabel="", title="")
    right_side = ax1.spines["right"]
    right_side.set_visible(False)
    top_side = ax1.spines["top"]
    top_side.set_visible(False)
    left_side = ax1.spines["left"]
    left_side.set_visible(False)
    ax1.tick_params(color="#626262", labelcolor="#626262")
    ax1.spines["bottom"].set_color("lightgrey")
    ax1.yaxis.grid(which="major", linestyle="-", linewidth="0.3", color="lightgrey")

    # summmarized per Category
    df_transaction = df_transaction[df_transaction.type_id != 3]  # take out investments
    df_transaction["Income"] = df_transaction["amount"][df_transaction.type_id == 2]
    df_transaction["Expenses"] = df_transaction["amount"][df_transaction.type_id == 1]
    g = df_transaction.groupby(["category_id"])  # group by category
    h = g.sum()
    h = h.reset_index()
    h = h[["category_id", "amount", "Income", "Expenses"]]
    df_category = df_category.set_index("id")
    summary_category = h.join(df_category, on="category_id", how="left").sort_values(
        "amount", ascending=True
    )

    # summmarized per Year
    df_transaction = df_transaction[df_transaction.type_id != 3]  # take out investments
    df_transaction["Income"] = df_transaction["amount"][df_transaction.type_id == 2]
    df_transaction["Expenses"] = df_transaction["amount"][df_transaction.type_id == 1]
    per = df_transaction.date.dt.to_period("Y")  # change notation to year
    g = df_transaction.groupby([per])  # group by year
    h = g.sum()
    h = h.reset_index()
    summary_year = h[["date", "amount", "Income", "Expenses"]].sort_values(
        "amount", ascending=False
    )

    # display chart
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(
        request,
        "myfinances/myfinances.html",
        {
            "data": uri,
            "transacties": transacties,
            "finance_list": finance_list,
            "filter": finance_filter,
            "summary_category": summary_category,
            "summary_year": summary_year,
        },
    )


def summary_cumul(request):

    finance_list = Transaction.objects.all()
    category_list = Category.objects.all()
    finance_filter = TransactionsFilter(request.GET, queryset=finance_list)
    finance_list = finance_filter.qs

    page = request.GET.get("page", 1)
    paginator = Paginator(finance_list, 100)

    try:
        transacties = paginator.page(page)
    except PageNotAnInteger:
        transacties = paginator.page(1)
    except EmptyPage:
        transacties = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "paginator": paginator,
        "filter": finance_filter,
        "is_paginated": True,
        "transacties": transacties,
        "finance_list": finance_list,
    }

    register_matplotlib_converters()  # function unknown
    # Say, 'the default sans-serif font is COMIC SANS'
    plt.rcParams["font.sans-serif"] = "Verdana"
    # Then, 'ALWAYS use sans-serif fonts'
    plt.rcParams["font.family"] = "sans-serif"

    # transform data
    q = finance_list.values()
    p = category_list.values()
    df_transaction = pd.DataFrame.from_records(q)
    df_category = pd.DataFrame.from_records(p)
    df_transaction["date"] = pd.to_datetime(df_transaction["date"])
    df_transaction = df_transaction.sort_values(by="date")
    df_transaction["date"] = df_transaction["date"].map(lambda dt: dt.replace(day=1))
    df_grouped = df_transaction.groupby(["date"])
    df_result = df_grouped.aggregate(np.sum)
    df_result["amount_cum"] = df_result.amount.cumsum()
    df_result = df_result.reset_index()
    fig, (ax1) = plt.subplots(
        1, sharex=True, gridspec_kw={"height_ratios": [3]}
    )  # 2 subplots, share x axis, different height size
    fig.set_size_inches(w=10, h=3)
    ax1.plot(df_result.date, df_result.amount_cum, color="lightgrey")
    ax1.xaxis.set_major_formatter(DateFormatter("%Y"))
    ax1.yaxis.set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, pos: "{:,.0f}".format(x) + "€")
    )
    ax1.set(xlabel="", ylabel="", title="")
    right_side = ax1.spines["right"]
    right_side.set_visible(False)
    top_side = ax1.spines["top"]
    top_side.set_visible(False)
    left_side = ax1.spines["left"]
    left_side.set_visible(False)
    ax1.tick_params(color="#626262", labelcolor="#626262")
    ax1.spines["bottom"].set_color("lightgrey")
    ax1.yaxis.grid(which="major", linestyle="-", linewidth="0.3", color="lightgrey")

    # summmarized per Category
    df_transaction = df_transaction[df_transaction.type_id != 3]  # take out investments
    df_transaction["Income"] = df_transaction["amount"][df_transaction.type_id == 2]
    df_transaction["Expenses"] = df_transaction["amount"][df_transaction.type_id == 1]
    g = df_transaction.groupby(["category_id"])  # group by category
    h = g.sum()
    h = h.reset_index()
    h = h[["category_id", "amount", "Income", "Expenses"]]
    df_category = df_category.set_index("id")
    summary_category = h.join(df_category, on="category_id", how="left").sort_values(
        "amount", ascending=True
    )

    # summmarized per Year
    df_transaction = df_transaction[df_transaction.type_id != 3]  # take out investments
    df_transaction["Income"] = df_transaction["amount"][df_transaction.type_id == 2]
    df_transaction["Expenses"] = df_transaction["amount"][df_transaction.type_id == 1]
    per = df_transaction.date.dt.to_period("Y")  # change notation to year
    g = df_transaction.groupby([per])  # group by year
    h = g.sum()
    h = h.reset_index()
    summary_year = h[["date", "amount", "Income", "Expenses"]].sort_values(
        "amount", ascending=False
    )

    # display chart
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(
        request,
        "myfinances/myfinances_cumul.html",
        {
            "data": uri,
            "transacties": transacties,
            "finance_list": finance_list,
            "filter": finance_filter,
            "summary_category": summary_category,
            "summary_year": summary_year,
        },
    )


class PostDetailView(DetailView):
    model = Transaction

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "file_list": Picture.objects.filter(
                    transaction_id=self.object.id
                ).order_by("id"),
            }
        )
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    form_class = PostForm
    success_url = "/myfinances"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return True


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = "/myfinances"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return True


class FileFieldView(FormView):
    form_class = PictureForm
    template_name = "myfinances/file_upload.html"
    success_url = "http://localhost:8000/myfinances/file/upload"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        files = request.FILES.getlist("file")
        if form.is_valid():
            transaction = form.cleaned_data["transaction"]
            i = 0
            for f in files:
                i += 1
                instance = Picture(file=f, transaction=transaction)
                instance.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {"form": form})
