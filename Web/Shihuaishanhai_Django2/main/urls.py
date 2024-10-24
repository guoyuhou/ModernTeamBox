from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('booking/<int:pk>/', views.BookingView.as_view(), name='booking'),
    path('booking/success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('facilities/', views.FacilityListView.as_view(), name='facilities'),
]
