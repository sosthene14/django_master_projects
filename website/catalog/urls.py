from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('pieces/', views.product_list, name='product_list'),
    path('collection/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('piece/<slug:slug>/', views.product_detail, name='product_detail'),
    path('philosophie/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('demande/', views.inquiry_submit, name='inquiry_submit'),
]
