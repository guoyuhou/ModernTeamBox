from django.template.loader import render_to_string

def render_header():
    return render_to_string('components/header.html')
