from django.template.loader import render_to_string

def render_footer():
    return render_to_string('components/footer.html')
