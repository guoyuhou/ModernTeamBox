from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('school-overview/', views.school_overview, name='school_overview'),
    path('teaching-research/', views.teaching_research, name='teaching_research'),
    path('teacher-growth/', views.teacher_growth, name='teacher_growth'),
    path('student-space/', views.student_space, name='student_space'),
    path('home-school-cooperation/', views.home_school_cooperation, name='home_school_cooperation'),
    path('teacher-development/', views.teacher_development, name='teacher_development'),
    path('party-building/', views.party_building, name='party_building'),
    path('admission-info/', views.admission_info, name='admission_info'),
]
