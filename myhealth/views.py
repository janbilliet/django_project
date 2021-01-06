from .models import Consultation, Medication
from django.shortcuts import render
from .filters import ConsultationFilter
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
from .fields import HealthForm, MedicationForm
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
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


def index_cons(request):
    consultation_list = Consultation.objects.all().order_by("-id")
    medication_list = Medication.objects.all().order_by("-id")
    consultation_filter = ConsultationFilter(request.GET, queryset=consultation_list)
    consultation_list = consultation_filter.qs
    paginator = Paginator(consultation_list, 10)
    page = request.GET.get("page")

    try:
        consultations = paginator.page(page)
    except PageNotAnInteger:
        consultations = paginator.page(1)
    except EmptyPage:
        consultations = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "paginator": paginator,
        "consultations": consultation_list,
        "medications": medication_list,
        "filter": consultation_filter,
        "is_paginated": True,
    }

    return render(
        request, "myhealth/myhealth_cons.html", context
    )


def index_med(request):
    consultation_list = Consultation.objects.all().order_by("-id")
    medication_list = Medication.objects.all().order_by("-id")
    consultation_filter = ConsultationFilter(request.GET, queryset=consultation_list)
    consultation_list = consultation_filter.qs
    paginator = Paginator(consultation_list, 10)
    page = request.GET.get("page")

    try:
        consultations = paginator.page(page)
    except PageNotAnInteger:
        consultations = paginator.page(1)
    except EmptyPage:
        consultations = paginator.page(paginator.num_pages)

    context = {
        "page": page,
        "paginator": paginator,
        "consultations": consultation_list,
        "medications": medication_list,
        "filter": consultation_filter,
        "is_paginated": True,
    }

    return render(
        request, "myhealth/myhealth_med.html", context
    )


class PostDetailView(DetailView):
    model = Consultation


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Consultation
    form_class = HealthForm
    success_url = "/myhealth/consultation"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        Medication = self.get_object()
        return True


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Consultation
    form_class = HealthForm
    success_url = "/myhealth/consultation"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        Medication = self.get_object()
        return True


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Consultation
    success_url = "/myhealth/medication"

    def test_func(self):
        return True


class MedicationDetailView(DetailView):
    model = Medication


class MedicationCreateView(LoginRequiredMixin, CreateView):
    model = Medication
    form_class = MedicationForm
    success_url = "/myhealth/medication"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        Medication = self.get_object()
        return True


class MedicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medication
    form_class = MedicationForm
    success_url = "/myhealth/medication"

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        Medication = self.get_object()
        return True


class MedicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medication
    success_url = "/myhealth/medication"

    def test_func(self):
        return True


def showchart(request):
    consultation_list = Consultation.objects.all().order_by("-id")
    medication_list = Medication.objects.all().order_by("-date")
    consultation_filter = ConsultationFilter(request.GET, queryset=consultation_list)
    consultation_list = consultation_filter.qs
    paginator = Paginator(consultation_list, 10)
    page = request.GET.get("page")

    try:
        consultations = paginator.page(page)
    except PageNotAnInteger:
        consultations = paginator.page(1)
    except EmptyPage:
        consultations = paginator.page(paginator.num_pages)

    register_matplotlib_converters()
    yearsFmt = mdates.DateFormatter("%Y")
    conn = sqlite3.connect("db.sqlite3")
    df = pd.read_sql_query(
        "select start_date,aantal_ochtend,aantal_avond,pijn from myhealth_medication;",
        conn,
    )

    # transform data
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["total"] = df["aantal_ochtend"] + df["aantal_avond"]

    # plot data
    fig1, (ax1) = plt.subplots(1, sharex=False, gridspec_kw={"height_ratios": [2]})
    fig1.set_size_inches(w=11, h=1.5)
    ax1.bar(
        df.start_date,
        df.aantal_avond,
        width=np.timedelta64(15, "h"),
        align="edge",
        bottom=df.aantal_ochtend,
        color="lightgrey",
    )
    ax1.bar(
        df.start_date,
        df.aantal_ochtend,
        width=np.timedelta64(15, "h"),
        align="edge",
        color="#848484",
    )
    # ax1.yaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax1.grid(axis="y", color="lightgrey")
    ax1.xaxis.set_visible(False)
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

    fig2, (ax2) = plt.subplots(1, sharex=False)
    fig2.set_size_inches(w=11, h=1)
    ax2.grid(axis="y", color="lightgrey")
    ax2.set(xlabel="", ylabel="", title="")
    ax2.xaxis.set_visible(False)
    ax2.bar(df.start_date, df.pijn, width=np.timedelta64(15, "h"), color="#FA5858")
    ax2.xaxis.set_major_formatter(DateFormatter("%Y"))
    right_side = ax2.spines["right"]
    right_side.set_visible(False)
    top_side = ax2.spines["top"]
    top_side.set_visible(False)
    left_side = ax2.spines["left"]
    left_side.set_visible(False)
    ax2.tick_params(color="#626262", labelcolor="#626262")
    ax2.spines["bottom"].set_color("lightgrey")
    ax2.yaxis.grid(which="major", linestyle="-", linewidth="0.3", color="lightgrey")

    # display chart
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri1 = urllib.parse.quote(string)

    buf = io.BytesIO()
    fig2.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri2 = urllib.parse.quote(string)

    context = {
        "page": page,
        "paginator": paginator,
        "consultations": consultation_list,
        "medications": medication_list,
        "filter": consultation_filter,
        "is_paginated": True,
        "data1": uri1,
        "data2": uri2,
    }

    return render(request, "myhealth/myhealth_graph.html", context)
