from django.contrib import admin
from django.utils.html import format_html
from .models import Room, Facility, Booking, Attraction

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'bed_type', 'max_guests', 'window', 'smoking']
    list_filter = ['smoking', 'window', 'floor']
    search_fields = ['name', 'description']

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon']
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'room', 'check_in', 'check_out', 'total_price', 'status']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['guest_name', 'phone']

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'distance', 'rating']
    list_filter = ['rating']
    search_fields = ['name', 'description']

# 自定义管理后台标题和头部
admin.site.site_header = '释怀山海民宿管理系统'
admin.site.site_title = '释怀山海民宿'
admin.site.index_title = '管理后台'
