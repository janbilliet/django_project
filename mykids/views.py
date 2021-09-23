from .models import DagboekPost, Video, Image, Mijlpaal, Tag
from .forms import PostForm, VideoForm, ImageForm, MijlpaalForm, TagForm
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
            rating = form.cleaned_data['rating']
            i=0
            for f in files:
                i+=1
                instance = Image(img=f,dagboekpost=dagboekpost,order=i,desc=desc,rating=rating)
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
            tag = form.cleaned_data['tag']
            i=0
            for f in files:
                i+=1
                instance = Video(vid=f,dagboekpost=dagboekpost,order=i,desc=desc,tag=tag,alltimefav=alltimefav,fav=fav)
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
				'dagboekpost_list_lotte':DagboekPost.objects.filter(id=self.object.id).filter(beschrijving_lotte__isnull=False).count(),		
				'dagboekpost_list_merlijn':DagboekPost.objects.filter(id=self.object.id).filter(beschrijving_merlijn__isnull=False).count(),	                
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
			dagboekposts = Video.objects.select_related('dagboekpost').filter(rating=3).order_by('?').all()[:10]
			context = {	
				'dagboekposts': dagboekposts,
			}
			return render(request, 'mykids/video_carousel.html', context)

def carousel_image(request): 
			dagboekposts_recent = Image.objects.select_related('dagboekpost').order_by('dagboekpost').all()[:25]
			dagboekposts_random = Image.objects.select_related('dagboekpost').order_by('?').all()[:25]
			dagboekposts_favourite = Image.objects.select_related('dagboekpost').filter(rating=2).order_by('?').all()[:25]
			dagboekposts_alltime_favourite = Image.objects.select_related('dagboekpost').filter(rating=3).order_by('?').all()[:25]			
			context = {	
				'dagboekposts_recent': dagboekposts_recent,
				'dagboekposts_random': dagboekposts_random,
				'dagboekposts_favourite': dagboekposts_favourite,
				'dagboekposts_alltime_favourite': dagboekposts_alltime_favourite,				
			}
			return render(request, 'mykids/image_carousel.html', context)

class MijlpaalCreateView(CreateView):
    model = Mijlpaal
    form_class = MijlpaalForm
