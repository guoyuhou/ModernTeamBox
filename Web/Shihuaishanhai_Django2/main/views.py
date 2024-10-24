from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Room, Facility, Booking, Attraction
from django.db.models import Q

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_rooms'] = Room.objects.all()[:3]  # 获取3个特色房间
        return context

class RoomListView(ListView):
    model = Room
    template_name = 'rooms.html'
    context_object_name = 'rooms'

class RoomDetailView(DetailView):
    model = Room
    template_name = 'detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facilities'] = self.object.facilities.all()
        return context

# 新增的视图
class FacilityListView(ListView):
    model = Facility
    template_name = 'facilities.html'
    context_object_name = 'facilities'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 按类别分组设施
        context['facility_categories'] = {
            'basic': Facility.objects.filter(category='basic'),
            'bathroom': Facility.objects.filter(category='bathroom'),
            'media': Facility.objects.filter(category='media'),
            'other': Facility.objects.filter(category='other')
        }
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attractions'] = Attraction.objects.all()
        return context

class BookingView(CreateView):
    model = Booking
    template_name = 'booking.html'
    fields = ['guest_name', 'phone', 'check_in', 'check_out', 'special_requests']  # 确保这些字段都在模型中存在
    success_url = reverse_lazy('main:booking_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = Room.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        # 保存预订信息到session
        self.request.session['room_id'] = self.kwargs['pk']
        self.request.session['guest_name'] = form.cleaned_data['guest_name']
        self.request.session['phone'] = form.cleaned_data['phone']
        self.request.session['check_in'] = form.cleaned_data['check_in'].strftime('%Y-%m-%d')
        self.request.session['check_out'] = form.cleaned_data['check_out'].strftime('%Y-%m-%d')
        self.request.session['special_requests'] = form.cleaned_data.get('special_requests', '')
        
        # 设置房间和计算总价
        form.instance.room = Room.objects.get(pk=self.kwargs['pk'])
        form.instance.total_price = form.instance.room.price
        
        return super().form_valid(form)

class BookingSuccessView(TemplateView):
    template_name = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = self.request.session.get('room_id')
        if room_id:
            try:
                context['room'] = Room.objects.get(id=room_id)
                context.update({
                    'check_in': self.request.session.get('check_in'),
                    'check_out': self.request.session.get('check_out'),
                    'guest_name': self.request.session.get('guest_name'),
                    'phone': self.request.session.get('phone'),
                    'special_requests': self.request.session.get('special_requests'),
                })
            except Room.DoesNotExist:
                pass
        return context
