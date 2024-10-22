from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from game import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('game/', include('game.urls')),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
