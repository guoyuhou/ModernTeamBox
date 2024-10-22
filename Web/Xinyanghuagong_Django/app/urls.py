from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),
    path('cooperation/', views.cooperation, name='cooperation'),
    path('certifications/', views.certifications, name='certifications'),
    path('company-data/', views.company_data, name='company_data'),
]