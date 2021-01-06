from django.urls import path
from . import views
from django.urls import include, path
from .views import (
	FileFieldView
)
urlpatterns = [
    path('myfinances', views.summary, name='transaction_home'),
    path('myfinances/cumul', views.summary_cumul, name='transaction_cumul_home'),
    path('myfinances/<int:pk>/', views.PostDetailView.as_view(), name='transaction_detail'),
    path('myfinances/new/transaction', views.TransactionCreateView.as_view(), name='transaction_add'),
	path('myfinances/new/type', views.TypeCreateView.as_view(), name='type_add'),
	path('myfinances/new/category', views.CategoryCreateView.as_view(), name='category_add'),
	path('myfinances/new/subcategory', views.SubcategoryCreateView.as_view(), name='subcategory_add'),
    path('myfinances/<int:pk>/update/', views.PostUpdateView.as_view(), name='transaction_update'),
    path('myfinances/<int:pk>/delete/', views.PostDeleteView.as_view(), name='transaction_delete'),
    path('ajax/load-categories/', views.load_categories, name='ajax_load_categories'), 
    path('ajax/load-subcategories/', views.load_subcategories, name='ajax_load_subcategories'), 
    path('myfinances/file/upload/', FileFieldView.as_view(), name = 'picture_add'),
]
