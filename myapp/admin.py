from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Student, Driver, Vehicle, Route, Stop, Schedule,
    Booking, Payment  # Removed VehicleLocation and Notification
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'get_full_name', 'phone_number', 'guardian_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'phone_number', 'guardian_name']
    readonly_fields = ['created_at', 'updated_at', 'display_profile_picture']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user', 'student_id', 'is_active')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'phone_number', 'address', 'profile_picture', 'display_profile_picture')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_contact')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="150" height="150" />')
        return "No image"
    display_profile_picture.short_description = 'Profile Picture Preview'


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['driver_id', 'get_full_name', 'license_number', 'phone_number', 'is_active', 'license_expiry']
    list_filter = ['is_active', 'created_at', 'license_expiry']
    search_fields = ['driver_id', 'user__first_name', 'user__last_name', 'license_number', 'phone_number']
    readonly_fields = ['created_at', 'updated_at', 'display_profile_picture']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user', 'driver_id', 'is_active')
        }),
        ('License Information', {
            'fields': ('license_number', 'license_expiry')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'profile_picture', 'display_profile_picture')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="150" height="150" />')
        return "No image"
    display_profile_picture.short_description = 'Profile Picture Preview'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'vehicle_type', 'model', 'capacity', 'driver_name', 'is_active']
    list_filter = ['vehicle_type', 'is_active']
    search_fields = ['plate_number', 'model', 'color']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('plate_number', 'vehicle_type', 'capacity')
        }),
        ('Details', {
            'fields': ('model', 'year', 'color', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def driver_name(self, obj):
        driver = obj.drivers.first()
        if driver:
            return driver.user.get_full_name()
        return "Unassigned"
    driver_name.short_description = 'Driver'


class StopInline(admin.TabularInline):
    model = Stop
    extra = 1
    fields = ['stop_order', 'stop_name', 'estimated_arrival_time']
    ordering = ['stop_order']


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    fields = ['day_of_week', 'departure_time', 'arrival_time', 'is_active']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['route_code', 'route_name', 'route_type', 'origin', 'destination', 'vehicle', 'fare', 'is_active']
    list_filter = ['route_type', 'is_active', 'created_at']
    search_fields = ['route_code', 'route_name', 'origin', 'destination']
    readonly_fields = ('created_at', 'updated_at')
    inlines = [StopInline, ScheduleInline]
    
    fieldsets = (
        ('Route Information', {
            'fields': ('route_name', 'route_code', 'route_type', 'is_active')
        }),
        ('Location', {
            'fields': ('origin', 'destination')
        }),
        ('Route Details', {
            'fields': ('distance_km', 'estimated_duration', 'fare')
        }),
        ('Vehicle Assignment', {
            'fields': ('vehicle',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    list_display = ['route', 'stop_order', 'stop_name', 'estimated_arrival_time']
    list_filter = ['route']
    search_fields = ['stop_name', 'route__route_name']
    ordering = ['route', 'stop_order']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['route', 'day_of_week', 'departure_time', 'arrival_time', 'is_active']
    list_filter = ['day_of_week', 'is_active', 'route']
    search_fields = ['route__route_name', 'route__route_code']
    ordering = ['route', 'day_of_week', 'departure_time']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'student_name', 'route', 'booking_date', 'status', 'total_fare', 'payment_status', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at']
    search_fields = ['booking_id', 'student__student_id', 'student__user__first_name', 'student__user__last_name']
    readonly_fields = ['booking_id', 'created_at', 'updated_at', 'payment_status_display']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'status')
        }),
        ('Student & Route', {
            'fields': ('student', 'route', 'schedule')
        }),
        ('Trip Details', {
            'fields': ('pickup_stop', 'dropoff_stop', 'booking_date', 'seats_booked')
        }),
        ('Payment', {
            'fields': ('total_fare', 'payment_status_display')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Student'
    
    def payment_status(self, obj):
        try:
            payment = obj.payment
            colors = {
                'COMPLETED': 'green',
                'PENDING': 'orange',
                'PROCESSING': 'blue',
                'FAILED': 'red',
                'REFUNDED': 'gray'
            }
            color = colors.get(payment.payment_status, 'black')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color,
                payment.get_payment_status_display()
            )
        except Payment.DoesNotExist:
            return format_html('<span style="color: red;">No Payment</span>')
    payment_status.short_description = 'Payment Status'
    
    def payment_status_display(self, obj):
        try:
            payment = obj.payment
            return f"{payment.get_payment_status_display()} - {payment.payment_method}"
        except Payment.DoesNotExist:
            return "No payment record"
    payment_status_display.short_description = 'Payment Info'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'booking_link', 'amount', 'payment_method', 'payment_status', 'payment_date', 'created_at']
    list_filter = ['payment_status', 'payment_method', 'payment_date', 'created_at']
    search_fields = ['payment_id', 'transaction_reference', 'booking__booking_id']
    readonly_fields = ['payment_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'booking', 'amount')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'payment_status', 'transaction_reference', 'payment_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def booking_link(self, obj):
        url = reverse('admin:myapp_booking_change', args=[obj.booking.id])
        return format_html('<a href="{}">{}</a>', url, obj.booking.booking_id)
    booking_link.short_description = 'Booking'


# Customize the admin site header and title
admin.site.site_header = "Sakay Transportation Admin"
admin.site.site_title = "Sakay Admin Portal"
admin.site.index_title = "Welcome to Sakay Transportation Management System"