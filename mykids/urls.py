from django.urls import path
from .views import (
    PostDetailView,
    ImageDetailView,
    VideoDetailView,
    PostCreateView,
    PostUpdateView,
    ImageUpdateView,
    VideoUpdateView,
    PostDeleteView,
    ImageDeleteView,
    VideoDeleteView,
    ImageFieldView,
    VideoFieldView,
    MijlpaalCreateView
)
from . import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    path('mykids/list', views.mykids_overview_list, name='mykids-home-list'),
    path('mykids/blog', views.mykids_overview_blog, name='mykids-home-blog'),
    path('mykids/image', views.mykids_image, name='mykids-image'),	
    path('mykids/video', views.mykids_video, name='mykids-video'),		
    path('mykids/<int:pk>/', PostDetailView.as_view(), name='mykids-detail'),
    path('mykids/new/', PostCreateView.as_view(), name='mykids-create'),
    path('mykids/image/upload/', ImageFieldView.as_view(), name = 'mykids-image-upload'),	
    path('mykids/video/upload/', VideoFieldView.as_view(), name = 'mykids-video-upload'),		
    path('mykids/image/<int:pk>/', ImageDetailView.as_view(), name = 'mykids-image-detail'),
    path('mykids/video/<int:pk>/', VideoDetailView.as_view(), name = 'mykids-video-detail'),	
    path('mykids/<int:pk>/update/', PostUpdateView.as_view(), name='mykids-update'),	
    path('mykids/image/<int:pk>/update/', ImageUpdateView.as_view(), name='mykids-image-update'),
    path('mykids/video/<int:pk>/update/', VideoUpdateView.as_view(), name='mykids-video-update'),	
    path('mykids/<int:pk>/delete/', PostDeleteView.as_view(), name='mykids-delete'),	
    path('mykids/image/<int:pk>/delete/', ImageDeleteView.as_view(), name='mykids-image-delete'),
    path('mykids/video/<int:pk>/delete/', VideoDeleteView.as_view(), name='mykids-video-delete'),
    path('mykids/video/recent', views.carousel_recent_video, name = 'carousel-recent-video'),	
    path('mykids/image/carousel', views.carousel_image, name = 'carousel-image'),
    path('mykids/video/random', views.carousel_random_video, name = 'carousel-random-video'),	
    path('mykids/video/favourite', views.carousel_favourite_video, name = 'carousel-favourite-video'),	
	path('mykids/new/milestone', views.MijlpaalCreateView.as_view(), name='milestone_add'),
]