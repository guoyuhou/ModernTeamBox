from django.contrib import admin
from .models import BlogPost, Service, Testimonial

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at')

admin.site.register(Service)
admin.site.register(Testimonial)
