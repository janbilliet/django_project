from .models import DagboekPost, Video, Image
from .forms import PostForm, VideoForm, ImageForm
from .filters import DagboekFilter, VideoFilter, ImageFilter
from django.shortcuts import render
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator
from django.template import Library
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO
import base64
import matplotlib.pyplot as plt
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
from django.views.generic.edit import FormView
from django.conf import settings

			
def mykids_overview_blog (request):

		dagboek_list = DagboekPost.objects.all()
		dagboek_filter = DagboekFilter(request.GET, queryset=dagboek_list)
		dagboek_list = dagboek_filter.qs

		page = request.GET.get('page',1)
		paginator = Paginator(dagboek_list, 50)
			
		try:
			dagboekposts = paginator.page(page)
		except PageNotAnInteger:
			dagboekposts = paginator.page(1)
		except EmptyPage:
			dagboekposts = paginator.page(paginator.num_pages)

		context = {
			'page': page,
			'paginator': paginator,			
			'filter': dagboek_filter,
			'is_paginated': True,
			'dagboekposts': dagboekposts,
			'dagboek_list': dagboek_list,
		}

		return render(request, 'mykids/mykids_blog.html', context)
		
def mykids_overview_list(request):

		dagboek_list = DagboekPost.objects.all()
		dagboek_filter = DagboekFilter(request.GET, queryset=dagboek_list)
		dagboek_list = dagboek_filter.qs	

		page = request.GET.get('page',1)
		paginator = Paginator(dagboek_list, 200)
			
		try:
			dagboekposts = paginator.page(page)
		except PageNotAnInteger:
			dagboekposts = paginator.page(1)
		except EmptyPage:
			dagboekposts = paginator.page(paginator.num_pages)

		context = {
			'page': page,
			'paginator': paginator,			
			'filter': dagboek_filter,
			'is_paginated': True,
			'dagboekposts': dagboekposts,
			'dagboek_list': dagboek_list,
		}

		return render(request, 'mykids/mykids_list.html', context)
				
def mykids_image(request):

		image_list = Image.objects.all()
		image_filter = ImageFilter(request.GET, queryset=image_list)
		image_list = image_filter.qs

		page = request.GET.get('page',1)
		paginator = Paginator(image_list, 365)
			
		try:
			imagefiles = paginator.page(page)
		except PageNotAnInteger:
			imagefiles = paginator.page(1)
		except EmptyPage:
			imagefiles = paginator.page(paginator.num_pages)

		context = {
			'page': page,
			'paginator': paginator,			
			'filter': image_filter,
			'is_paginated': True,
			'imagefiles': imagefiles,
			'image_list': image_list,
		}

		return render(request, 'mykids/mykids_image.html', context)
		
def mykids_video(request):

		video_list = Video.objects.all()
		video_filter = VideoFilter(request.GET, queryset=video_list)
		video_list = video_filter.qs

		page = request.GET.get('page',1)
		paginator = Paginator(video_list, 10)
			
		try:
			videofiles = paginator.page(page)
		except PageNotAnInteger:
			videofiles = paginator.page(1)
		except EmptyPage:
			videofiles = paginator.page(paginator.num_pages)

		context = {
			'page': page,
			'paginator': paginator,			
			'filter': video_filter,
			'is_paginated': True,
			'videofiles': videofiles,
			'video_list': video_list,
		}

		return render(request, 'mykids/mykids_video.html', context)

class ImageFieldView(FormView):
    form_class = ImageForm
    template_name = 'mykids/file_upload.html'  
    success_url = '/mykids/image/upload/'
	
         
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        files = request.FILES.getlist('img')
        if form.is_valid():
            desc = form.cleaned_data['desc']
            dagboekpost = form.cleaned_data['dagboekpost']
            fav = form.cleaned_data['fav']
            alltimefav = form.cleaned_data['alltimefav']
            name = form.cleaned_data['name']
            i=0
            for f in files:
                i+=1
                instance = Image(img=f,dagboekpost=dagboekpost,order=i,desc=desc,name=name,alltimefav=alltimefav,fav=fav)
                instance.save()    
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})

class VideoFieldView(FormView):
    form_class = VideoForm
    template_name = 'mykids/file_upload.html'  
    success_url = '/mykids/video/upload/'
         
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        files = request.FILES.getlist('vid')
        if form.is_valid():
            desc = form.cleaned_data['desc']
            dagboekpost = form.cleaned_data['dagboekpost']
            fav = form.cleaned_data['fav']
            alltimefav = form.cleaned_data['alltimefav']
            name = form.cleaned_data['name']
            i=0
            for f in files:
                i+=1
                instance = Video(vid=f,dagboekpost=dagboekpost,order=i,desc=desc,name=name,alltimefav=alltimefav,fav=fav)
                instance.save()    
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})

class PostDetailView(DetailView):
    model = DagboekPost

    def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
				'image_list':Image.objects.filter(dagboekpost_id=self.object.id).order_by('order'),
				'video_list':Video.objects.filter(dagboekpost_id=self.object.id).order_by('order'),				
				})
        return context
		
class ImageDetailView(DetailView):
	model = Image
	success_url = '/mykids/image/'
	
class VideoDetailView(DetailView):
	model = Video
	success_url = '/mykids/video/'
	
class PostCreateView(LoginRequiredMixin, CreateView):
    model = DagboekPost
    form_class = PostForm

    def form_valid(self, form):
        return super().form_valid(form)
	
    def test_func(self):
        post = self.get_object()
        return True		
					
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DagboekPost
    form_class = PostForm

    def form_valid(self, form):
        print(form.is_valid())
        return super().form_valid(form)
	
    def test_func(self):
        post = self.get_object()
        return True

class ImageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Image
    form_class = ImageForm

    def form_valid(self, form):
        return super().form_valid(form)
	
    def test_func(self):
        post = self.get_object()
        return True

class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    form_class = VideoForm

    def form_valid(self, form):
        return super().form_valid(form)
	
    def test_func(self):
        post = self.get_object()
        return True

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DagboekPost
    success_url = '/mykids/list'

    def form_valid(self, form):
        return super().form_valid(form)
	
    def test_func(self):
        post = self.get_object()
        return True
		
class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Image
    success_url = '/mykids/image'

    def form_valid(self, form):
        return super().form_valid(form)
	
    def test_func(self):
        post = self.get_object()
        return True

class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    success_url = '/mykids/video'

    def form_valid(self, form):
        return super().form_valid(form)
	
    def test_func(self):
        post = self.get_object()
        return True

def showchart(request):
    register_matplotlib_converters() #function unknown
    yearsFmt = mdates.DateFormatter('%Y')
    conn = sqlite3.connect("db.sqlite3")
    df = pd.read_sql_query("select datum,uurvanSlapen,uurvanOpstaan,nachtflesjes from mykids_dagboekpost;", conn)
	
	#transform data
    df = df[df.uurvanOpstaan != 'NULL']
    df = df[df.uurvanSlapen != 'NULL']
    df = df.dropna()
    df['uurvanOpstaan'] = df['uurvanOpstaan'].str.replace("u", ":")
    df['uurvanSlapen'] = df['uurvanSlapen'].str.replace("u", ":")
    df['uurvanOpstaan'] = np.where(df.uurvanOpstaan.str.contains('-'), '2019-04-22' + ' ' + df['uurvanOpstaan'].str[10:], '2019-04-22' + ' ' +  df['uurvanOpstaan'] + ':00')
    df['uurvanSlapen'] = np.where(df.uurvanSlapen.str.contains('-'), '2019-04-22' + ' ' + df['uurvanSlapen'].str[10:], '2019-04-22' + ' ' +  df['uurvanSlapen'] + ':00')

    df['datum']= pd.to_datetime(df['datum'])
    df['uurvanOpstaan']= pd.to_datetime(df['uurvanOpstaan'])
    df['uurvanSlapen']= pd.to_datetime(df['uurvanSlapen'])
		
	#plot data
    fig, (ax1,ax2) = plt.subplots(2, sharex=False,gridspec_kw={'height_ratios': [6, 1]}) # 2 subplots, share x axis, different height size
    fig.set_size_inches(w=11,h=7)
    ax1.plot(df.datum,df.uurvanOpstaan,'s',  markersize=3) #scatter plot
    ax1.plot(df.datum,df.uurvanSlapen,'s',  markersize=3)  #scatter plot
    ax1.set(xlabel='', ylabel='',title='Evolutie uur van opstaan & gaan slapen')
    ax1.yaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax1.set_ylim([pd.to_datetime('2019-04-22 00:00:00'), pd.to_datetime('2019-04-22 23:00:00')])
    ax1.set_xlim(left=pd.to_datetime('2019-09-01 00:00:00'))
    ax1.grid(axis='y',color='lightgrey')
    ticks = ['22-04-2019 00:00:00','22-04-2019 04:00:00','22-04-2019 05:00:00','22-04-2019 06:00:00','22-04-2019 07:00:00','22-04-2019 08:00:00','22-04-2019 16:00:00','22-04-2019 17:00:00','22-04-2019 18:00:00','22-04-2019 19:00:00','22-04-2019 20:00:00','22-04-2019 21:00:00']
    ax1.set_yticks(ticks)
    ax2.plot(df.datum,df.nachtflesjes,'s',  markersize=2, c='grey')
	
	#display chart
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request,'mykids/chart_evolutie.html',{'data':uri})		
	

def carousel_random_video(request): 
			dagboekposts = Video.objects.select_related('dagboekpost').order_by('?').all()[:10]
			context = {	
				'dagboekposts': dagboekposts,
			}
			return render(request, 'mykids/video_carousel.html', context)
			
def carousel_recent_video(request): 
			dagboekposts = Video.objects.select_related('dagboekpost').order_by('dagboekpost_id').all()[:10]
			context = {	
				'dagboekposts': dagboekposts,
			}
			return render(request, 'mykids/video_carousel.html', context)		
		
def carousel_favourite_video(request): 
			dagboekposts = Video.objects.select_related('dagboekpost').filter(fav=1).order_by('?').all()[:10]
			context = {	
				'dagboekposts': dagboekposts,
			}
			return render(request, 'mykids/video_carousel.html', context)

def carousel_image(request): 
			dagboekposts_recent = Image.objects.select_related('dagboekpost').order_by('dagboekpost').all()[:25]
			dagboekposts_random = Image.objects.select_related('dagboekpost').order_by('?').all()[:25]
			dagboekposts_favourite = Image.objects.select_related('dagboekpost').filter(fav=1).order_by('?').all()[:25]
			dagboekposts_alltime_favourite = Image.objects.select_related('dagboekpost').filter(alltimefav=1).order_by('?').all()[:25]			
			context = {	
				'dagboekposts_recent': dagboekposts_recent,
				'dagboekposts_random': dagboekposts_random,
				'dagboekposts_favourite': dagboekposts_favourite,
				'dagboekposts_alltime_favourite': dagboekposts_alltime_favourite,				
			}
			return render(request, 'mykids/image_carousel.html', context)