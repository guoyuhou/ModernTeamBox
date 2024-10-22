from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
import json

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def products(request):
    return render(request, 'products.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # 发送邮件
            send_mail(
                f'新的联系表单提交: {subject}',
                f'姓名: {name}\n邮箱: {email}\n\n消息:\n{message}',
                email,
                ['your-email@xinyang-chem.com'],  # 替换为您的邮箱
                fail_silently=False,
            )
            
            messages.success(request, '您的消息已成功发送，我们会尽快回复您。')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def cooperation(request):
    return render(request, 'cooperation.html')

def certifications(request):
    return render(request, 'certifications.html')

def company_data(request):
    # 这里我们模拟一些公司数据
    data = {
        'annual_production': [
            {'year': 2016, 'value': 50000},
            {'year': 2017, 'value': 60000},
            {'year': 2018, 'value': 75000},
            {'year': 2019, 'value': 90000},
            {'year': 2020, 'value': 100000},
        ],
        'carbon_reduction': [
            {'year': 2016, 'value': 1000},
            {'year': 2017, 'value': 1500},
            {'year': 2018, 'value': 2200},
            {'year': 2019, 'value': 3000},
            {'year': 2020, 'value': 4000},
        ],
        'customer_satisfaction': [
            {'year': 2016, 'value': 85},
            {'year': 2017, 'value': 87},
            {'year': 2018, 'value': 90},
            {'year': 2019, 'value': 92},
            {'year': 2020, 'value': 95},
        ],
    }
    return render(request, 'company_data.html', {'data': json.dumps(data)})
