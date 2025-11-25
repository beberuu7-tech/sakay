# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class ThreeTierAccessMiddleware:
    """
    Middleware to enforce three-tier role-based access control.
    Separates Admin, Driver, and Student access.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Define admin-only URLs
        self.admin_urls = [
            '/admin/dashboard/',
            '/admin/bookings/',
            '/admin/routes/',
            '/admin/students/',
            '/admin/drivers/',
            '/admin/vehicles/',
            '/admin/trips/',
            '/admin/reports/',
            '/admin/settings/',
        ]
        
        # Define driver-only URLs
        self.driver_urls = [
            '/driver/dashboard/',
            '/driver/trips/',
            '/driver/schedule/',
            '/driver/earnings/',
            '/driver/profile/',
        ]
        
        # Define student-only URLs
        self.student_urls = [
            '/dashboard/',
            '/profile/',
            '/bookings/',
            '/book/',
            '/booking/',
        ]
        
        # Public URLs (accessible by anyone, even unauthenticated)
        self.public_urls = [
            '/login/',
            '/register/',
            '/logout/',
        ]
    
    def is_admin(self, user):
        return user.is_staff or user.is_superuser
    
    def is_driver(self, user):
        return hasattr(user, 'driver')
    
    def is_student(self, user):
        return hasattr(user, 'student')
    
    def __call__(self, request):
        path = request.path
        
        # Allow public URLs without authentication
        if any(path.startswith(url) for url in self.public_urls):
            return self.get_response(request)
        
        # Allow static and media files
        if path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)
        
        # Allow Django admin panel
        if path.startswith('/admin/') and not path.startswith('/admin/dashboard'):
            return self.get_response(request)
        
        # If user is not authenticated, let Django's LOGIN_REQUIRED handle it
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Determine user type
        is_admin = self.is_admin(request.user)
        is_driver = self.is_driver(request.user)
        is_student = self.is_student(request.user)
        
        # ADMIN ACCESS CONTROL
        if is_admin:
            # Admins can access admin URLs
            if any(path.startswith(url) for url in self.admin_urls):
                return self.get_response(request)
            
            # Block admins from driver-only pages
            if any(path.startswith(url) for url in self.driver_urls):
                messages.warning(request, 'Access denied. This page is for drivers only.')
                return redirect('admin_dashboard')
            
            # Block admins from student-only pages (except viewing)
            if any(path.startswith(url) for url in self.student_urls):
                # Allow admins to view bookings and student data
                if '/booking/' in path or '/profile/' in path:
                    return self.get_response(request)
                messages.warning(request, 'Access denied. This page is for students only.')
                return redirect('admin_dashboard')
        
        # DRIVER ACCESS CONTROL
        elif is_driver:
            # Drivers can access driver URLs
            if any(path.startswith(url) for url in self.driver_urls):
                return self.get_response(request)
            
            # Allow drivers to view their assigned bookings
            if '/booking/' in path or '/track/' in path:
                return self.get_response(request)
            
            # Block drivers from admin pages
            if any(path.startswith(url) for url in self.admin_urls):
                messages.error(request, 'You do not have permission to access admin pages.')
                return redirect('driver_dashboard')
            
            # Block drivers from creating bookings
            if path.startswith('/book/') or path == '/bookings/':
                messages.warning(request, 'Drivers cannot create bookings.')
                return redirect('driver_dashboard')
        
        # STUDENT ACCESS CONTROL
        elif is_student:
            # Students can access student URLs
            if any(path.startswith(url) for url in self.student_urls):
                return self.get_response(request)
            
            # Allow students to access routes, about, contact
            if path.startswith('/routes/') or path == '/about/' or path == '/contact/':
                return self.get_response(request)
            
            # Allow students to track their bookings
            if '/track/' in path:
                return self.get_response(request)
            
            # Block students from admin pages
            if any(path.startswith(url) for url in self.admin_urls):
                messages.error(request, 'You do not have permission to access admin pages.')
                return redirect('dashboard')
            
            # Block students from driver-only pages
            if any(path.startswith(url) for url in self.driver_urls):
                messages.warning(request, 'Access denied. This page is for drivers only.')
                return redirect('dashboard')
        
        # If no profile found, redirect to login
        else:
            messages.error(request, 'User profile not found. Please contact support.')
            return redirect('login')
        
        # Allow access to other pages (like home which will auto-redirect)
        response = self.get_response(request)
        return response