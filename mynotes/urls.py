from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('mynotes', views.home, name='mynotes-home'),
    path('mynotes/<int:pk>/', PostDetailView.as_view(), name='mynotes-detail'),
    path('mynotes/new/', PostCreateView.as_view(), name='mynotes-create'),
    path('mynotes/<int:pk>/update/', PostUpdateView.as_view(), name='mynotes-update'),
    path('mynotes/<int:pk>/delete/', PostDeleteView.as_view(), name='mynotes-delete')
]