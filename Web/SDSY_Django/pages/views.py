from django.shortcuts import render
import json

def load_content():
    with open('data/content.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def index(request):
    content = load_content()
    return render(request, 'index.html', {'content': content['index']})

def school_overview(request):
    content = load_content()
    return render(request, 'school_overview.html', {'content': content['school_overview']})

def teaching_research(request):
    content = load_content()
    return render(request, 'teaching_research.html', {'content': content['teaching_research']})

def teacher_growth(request):
    content = load_content()
    return render(request, 'teacher_growth.html', {'content': content['teacher_growth']})

def student_space(request):
    content = load_content()
    return render(request, 'student_space.html', {'content': content['student_space']})

def home_school_cooperation(request):
    content = load_content()
    return render(request, 'home_school_cooperation.html', {'content': content['home_school_cooperation']})

def teacher_development(request):
    content = load_content()
    return render(request, 'teacher_development.html', {'content': content['teacher_development']})

def party_building(request):
    content = load_content()
    return render(request, 'party_building.html', {'content': content['party_building']})

def admission_info(request):
    content = load_content()
    return render(request, 'admission_info.html', {'content': content['admission_info']})
