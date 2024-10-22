import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shandong_university_affiliated_school.settings')

application = get_wsgi_application()
