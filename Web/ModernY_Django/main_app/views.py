from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Service, Testimonial
import random

def home(request):
    services = [
        {
            'icon': 'fas fa-robot',
            'title': '人工智能解决方案',
            'description': '为您的业务提供智能化升级，提高效率和决策能力。',
            'id': 1
        },
        {
            'icon': 'fas fa-vr-cardboard',
            'title': '虚拟现实体验',
            'description': '创造身临其境的虚拟世界，为您的产品或服务增添全新维度。',
            'id': 2
        },
        {
            'icon': 'fas fa-cloud',
            'title': '云计算服务',
            'description': '灵活、安全的云端解决方案，助力您的业务快速扩展。',
            'id': 3
        }
    ]
    
    testimonials = [
        {
            'content': 'ModernY的服务让我们的生产效率提高了30%，非常满意！',
            'author': '张三',
            'position': 'CEO',
            'company': 'ABC科技',
            'avatar_url': 'https://randomuser.me/api/portraits/men/1.jpg'
        },
        {
            'content': '他们的虚拟现实解决方案为我们的产品展示带来了革命性的变化。',
            'author': '李四',
            'position': '市场总监',
            'company': 'XYZ创新',
            'avatar_url': 'https://randomuser.me/api/portraits/women/1.jpg'
        },
        {
            'content': 'ModernY的云服务帮助我们轻松应对了业务高速增长带来的挑战。',
            'author': '王五',
            'position': 'CTO',
            'company': '未来科技',
            'avatar_url': 'https://randomuser.me/api/portraits/men/2.jpg'
        }
    ]
    
    return render(request, 'home.html', {'services': services, 'testimonials': testimonials})

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def products(request):
    return render(request, 'products.html')

def careers(request):
    return render(request, 'careers.html')

def contact(request):
    return render(request, 'contact.html')

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')  
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog_detail.html', {'post': post})

def privacy(request):
    return render(request, 'main_app/privacy.html')

def terms(request):
    return render(request, 'main_app/terms.html')
