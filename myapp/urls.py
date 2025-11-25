from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ============ PUBLIC ROUTES ============
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('routes/', views.routes_list, name='routes_list'),
    path('routes/<str:route_code>/', views.route_detail, name='route_detail'),

# ============ AUTHENTICATION ============
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('register/choice/', views.register_choice, name='register'),
path('register/student/', views.student_register, name='student_register'),
path('register/driver/', views.driver_register, name='driver_register'),

    # ============ STUDENT ROUTES ============
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    # Bookings (Student)
    path('book/<str:route_code>/', views.create_booking, name='create_booking'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<str:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<str:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),

    # ============ TRACKING (All Users) ============
    path('track/<str:booking_id>/', views.track_booking, name='track_booking'),
    path('live-map/', views.live_map, name='live_map'),
    path('api/vehicle-location/<int:vehicle_id>/', views.get_vehicle_location, name='get_vehicle_location'),
    path('api/update-location/', views.update_vehicle_location, name='update_vehicle_location'),

    # ============ DRIVER ROUTES ============
    path('driver/dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('driver/trips/', views.driver_trips, name='driver_trips'),
    path('driver/trips/<int:trip_id>/', views.driver_trip_detail, name='driver_trip_detail'),
    path('driver/trips/<int:trip_id>/start/', views.driver_start_trip, name='driver_start_trip'),
    path('driver/trips/<int:trip_id>/complete/', views.driver_complete_trip, name='driver_complete_trip'),
    path('driver/schedule/', views.driver_schedule, name='driver_schedule'),
    path('driver/earnings/', views.driver_earnings, name='driver_earnings'),
    path('driver/profile/', views.driver_profile, name='driver_profile'),

    # ============ ADMIN ROUTES (RENAMED) ============
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    # Bookings (Admin)
    path('dashboard/admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('dashboard/admin/bookings/<str:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),
    path('dashboard/admin/bookings/<str:booking_id>/confirm/', views.admin_confirm_booking, name='admin_confirm_booking'),

    # Routes (Admin)
    path('dashboard/admin/routes/', views.admin_routes, name='admin_routes'),
    path('dashboard/admin/routes/add/', views.admin_add_route, name='admin_add_route'),

    # Students (Admin)
    path('dashboard/admin/students/', views.admin_students, name='admin_students'),

    # Drivers (Admin)
    path('dashboard/admin/drivers/', views.admin_drivers, name='admin_drivers'),
    path('dashboard/admin/drivers/<int:driver_id>/approve/', views.admin_approve_driver, name='admin_approve_driver'),

    # Vehicles (Admin)
    path('dashboard/admin/vehicles/', views.admin_vehicles, name='admin_vehicles'),
    path('dashboard/admin/vehicles/add/', views.admin_add_vehicle, name='admin_add_vehicle'),

    # Trips (Admin)
    path('dashboard/admin/trips/', views.admin_trips, name='admin_trips'),
    path('dashboard/admin/trips/<int:trip_id>/assign/', views.admin_assign_driver, name='admin_assign_driver'),

    # Reports & Settings (Admin)
    path('dashboard/admin/reports/', views.admin_reports, name='admin_reports'),
    path('dashboard/admin/settings/', views.admin_settings, name='admin_settings'),

    path('terms/', views.terms, name='terms'),
]
