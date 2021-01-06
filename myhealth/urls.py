from django.urls import path
from .views import (
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    MedicationDetailView,
    MedicationCreateView,
    MedicationUpdateView,
    MedicationDeleteView
)
from . import views

urlpatterns = [
    path('myhealth/consultation', views.index_cons, name='myhealth_home'),
    path('myhealth/medication', views.index_med, name='medication_home'),	
    path('myhealth/graphs', views.showchart, name='medication_graphs'),	
    path('myhealth/<int:pk>/', PostDetailView.as_view(), name='myhealth_detail'),
    path('myhealth/new/', PostCreateView.as_view(), name='myhealth_create'),
    path('myhealth/<int:pk>/update/', PostUpdateView.as_view(), name='myhealth_update'),
    path('myhealth/<int:pk>/delete/', PostDeleteView.as_view(), name='myhealth_delete'),
    path('myhealth/medication/<int:pk>/', MedicationDetailView.as_view(), name='medication_detail'),
    path('myhealth/medication/new/', MedicationCreateView.as_view(), name='medication_create'),
    path('myhealth/medication/<int:pk>/update/', MedicationUpdateView.as_view(), name='medication_update'),
    path('myhealth/medication/<int:pk>/delete/', MedicationDeleteView.as_view(), name='medication_delete'),
]
