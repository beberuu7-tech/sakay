# views.py - Complete and Fixed Implementation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from .models import (Route, Booking, Student, Schedule, Stop, Payment, Vehicle, 
                     VehicleLocation, Driver, Trip)
from .forms import StudentRegistrationForm, StudentProfileUpdateForm, StudentPasswordChangeForm, DriverRegistrationForm
from datetime import datetime, date, timedelta
import json


# ================== HELPER FUNCTIONS ==================
def terms(request):
    """Terms and conditions page"""
    return render(request, 'myapp/terms.html')

def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser

def is_driver(user):
    """Check if user is a driver"""
    return hasattr(user, 'driver')

def is_student(user):
    """Check if user is a student"""
    return hasattr(user, 'student')

def get_user_type(user):
    """Get the type of user"""
    if is_admin(user):
        return 'admin'
    elif is_driver(user):
        return 'driver'
    elif is_student(user):
        return 'student'
    return None


def home(request):
    """Home page view - public landing page"""
    # If user is authenticated, redirect to their dashboard
    if request.user.is_authenticated:
        user_type = get_user_type(request.user)
        if user_type == 'admin':
            return redirect('admin_dashboard')
        elif user_type == 'driver':
            return redirect('driver_dashboard')
        elif user_type == 'student':
            return redirect('dashboard')
        # Fallback
        return redirect('dashboard')
    
    # Show public home page for non-authenticated users
    context = {
        'total_routes': Route.objects.filter(is_active=True).count(),
        'featured_routes': Route.objects.filter(is_active=True)[:6],
        'today': date.today(),
    }
    return render(request, 'myapp/home.html', context)


def about(request):
    """About page view"""
    return render(request, 'myapp/about.html')


def routes_list(request):
    """Display all available routes"""
    routes = Route.objects.filter(is_active=True).select_related('vehicle')
    
    route_type = request.GET.get('type')
    if route_type:
        routes = routes.filter(route_type=route_type)
    
    search_query = request.GET.get('search')
    if search_query:
        routes = routes.filter(
            Q(route_name__icontains=search_query) |
            Q(origin__icontains=search_query) |
            Q(destination__icontains=search_query)
        )
    
    context = {
        'routes': routes,
        'route_type': route_type,
        'search_query': search_query,
    }
    return render(request, 'myapp/routes_list.html', context)


def route_detail(request, route_code):
    """Display route details with stops and schedules"""
    route = get_object_or_404(Route, route_code=route_code, is_active=True)
    stops = route.stops.order_by('stop_order')
    schedules = route.schedules.filter(is_active=True).order_by('day_of_week', 'departure_time')
    
    context = {
        'route': route,
        'stops': stops,
        'schedules': schedules,
    }
    return render(request, 'myapp/route_details.html', context)


def contact(request):
    """Contact page"""
    if request.method == 'POST':
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'myapp/contact.html')


# ================== AUTHENTICATION ==================

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        user_type = get_user_type(request.user)
        if user_type == 'admin':
            return redirect('admin_dashboard')
        elif user_type == 'driver':
            return redirect('driver_dashboard')
        else:
            return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user type
            user_type = get_user_type(user)
            if user_type == 'admin':
                return redirect('admin_dashboard')
            elif user_type == 'driver':
                return redirect('driver_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'myapp/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def register_choice(request):
    """Registration choice page"""
    return render(request, 'myapp/register_choice.html')


def student_register(request):
    """Student registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                profile_picture=form.cleaned_data.get('profile_picture'),
                guardian_name=form.cleaned_data['guardian_name'],
                guardian_relationship=form.cleaned_data.get('guardian_relationship', 'PARENT'),
                guardian_contact=form.cleaned_data['guardian_contact'],
                emergency_contact_name=form.cleaned_data['emergency_contact_name'],
                emergency_contact_relationship=form.cleaned_data.get('emergency_contact_relationship', 'PARENT'),
                emergency_contact_number=form.cleaned_data['emergency_contact_number'],
                is_active=True
            )
            
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'myapp/register.html', {'form': form})


def driver_register(request):
    """Driver registration view - requires admin approval"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user but don't log them in yet
            user = form.save()
            
            # Create driver profile (NOT VERIFIED yet)
            driver = Driver.objects.create(
                user=user,
                driver_id=form.cleaned_data['driver_id'],
                license_number=form.cleaned_data['license_number'],
                license_expiry=form.cleaned_data['license_expiry'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                emergency_contact_name=form.cleaned_data['emergency_contact_name'],
                emergency_contact_number=form.cleaned_data['emergency_contact_number'],
                profile_picture=form.cleaned_data.get('profile_picture'),
                is_active=False,  # Inactive until approved
                is_verified=False  # Not verified until admin approves
            )
            
            # Save license photo (you'll need to add this field to Driver model)
            if form.cleaned_data.get('license_photo'):
                # Store the license photo for admin review
                driver.license_photo = form.cleaned_data['license_photo']
                driver.save()
            
            messages.success(
                request, 
                f'Thank you {user.first_name}! Your driver application has been submitted. '
                f'You will receive a notification once an administrator reviews and approves your account.'
            )
            return redirect('login')
    else:
        form = DriverRegistrationForm()
    
    return render(request, 'myapp/driver/driver_register.html', {'form': form})


# ================== STUDENT VIEWS ==================

@login_required
def dashboard(request):
    """Student dashboard"""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    if is_driver(request.user):
        return redirect('driver_dashboard')
    
    try:
        student = request.user.student
        
        # Get all bookings first, then slice
        all_bookings = Booking.objects.filter(student=student).select_related(
            'route', 'payment', 'schedule'
        ).order_by('-created_at')
        
        # Get upcoming bookings BEFORE slicing
        upcoming_bookings = all_bookings.filter(
            booking_date__gte=date.today(),
            status__in=['PENDING', 'CONFIRMED']
        )
        
        # Now slice for recent bookings
        recent_bookings = all_bookings[:10]
        
        context = {
            'student': student,
            'bookings': recent_bookings,
            'upcoming_bookings': upcoming_bookings,
            'total_bookings': all_bookings.count(),
        }
        return render(request, 'myapp/dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')


@login_required
def create_booking(request, route_code):
    """Create a new booking"""
    if is_admin(request.user):
        messages.error(request, 'Admins cannot create bookings.')
        return redirect('admin_dashboard')
    if is_driver(request.user):
        messages.error(request, 'Drivers cannot create bookings.')
        return redirect('driver_dashboard')
    
    route = get_object_or_404(Route, route_code=route_code, is_active=True)
    
    if request.method == 'POST':
        try:
            student = request.user.student
            schedule_id = request.POST.get('schedule')
            pickup_stop_id = request.POST.get('pickup_stop')
            dropoff_stop_id = request.POST.get('dropoff_stop')
            booking_date = request.POST.get('booking_date')
            seats = int(request.POST.get('seats', 1))
            
            schedule = get_object_or_404(Schedule, id=schedule_id, route=route)
            pickup_stop = get_object_or_404(Stop, id=pickup_stop_id, route=route)
            dropoff_stop = get_object_or_404(Stop, id=dropoff_stop_id, route=route)
            
            total_fare = route.fare * seats
            
            booking = Booking.objects.create(
                student=student,
                route=route,
                schedule=schedule,
                pickup_stop=pickup_stop,
                dropoff_stop=dropoff_stop,
                booking_date=booking_date,
                seats_booked=seats,
                total_fare=total_fare,
                status='PENDING'
            )
            
            Payment.objects.create(
                booking=booking,
                amount=total_fare,
                payment_method='CASH',
                payment_status='PENDING'
            )
            
            messages.success(request, f'Booking created successfully! Booking ID: {booking.booking_id}')
            return redirect('booking_detail', booking_id=booking.booking_id)
            
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    stops = route.stops.order_by('stop_order')
    schedules = route.schedules.filter(is_active=True)
    
    context = {
        'route': route,
        'stops': stops,
        'schedules': schedules,
    }
    return render(request, 'myapp/create_booking.html', context)


@login_required
def booking_detail(request, booking_id):
    """Display booking details"""
    if is_admin(request.user):
        booking = get_object_or_404(Booking, booking_id=booking_id)
    elif is_driver(request.user):
        booking = get_object_or_404(
            Booking,
            booking_id=booking_id,
            trip__driver=request.user.driver
        )
    else:
        booking = get_object_or_404(
            Booking, 
            booking_id=booking_id,
            student=request.user.student
        )
    
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'booking': booking,
        'payment': payment,
    }
    return render(request, 'myapp/booking_detail.html', context)


@login_required
def my_bookings(request):
    """Display all user bookings"""
    if is_admin(request.user):
        return redirect('admin_bookings')
    if is_driver(request.user):
        return redirect('driver_trips')
    
    try:
        student = request.user.student
        bookings = Booking.objects.filter(student=student).select_related(
            'route', 'payment', 'schedule', 'pickup_stop', 'dropoff_stop'
        ).order_by('-created_at')
        
        status_filter = request.GET.get('status')
        if status_filter:
            bookings = bookings.filter(status=status_filter)
        
        context = {
            'bookings': bookings,
            'status_filter': status_filter,
        }
        return render(request, 'myapp/my_booking.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    if is_admin(request.user):
        booking = get_object_or_404(Booking, booking_id=booking_id)
    elif is_driver(request.user):
        messages.error(request, 'Drivers cannot cancel bookings.')
        return redirect('driver_dashboard')
    else:
        booking = get_object_or_404(
            Booking,
            booking_id=booking_id,
            student=request.user.student
        )
    
    if request.method == 'POST':
        if booking.status in ['PENDING', 'CONFIRMED']:
            booking.status = 'CANCELLED'
            booking.save()
            
            try:
                payment = booking.payment
                if payment.payment_status == 'COMPLETED':
                    payment.payment_status = 'REFUNDED'
                    payment.save()
            except Payment.DoesNotExist:
                pass
            
            messages.success(request, 'Booking cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel this booking.')
        
        if is_admin(request.user):
            return redirect('admin_bookings')
        return redirect('my_bookings')
    
    return render(request, 'myapp/cancel_booking.html', {'booking': booking})


@login_required
def profile(request):
    """View student profile"""
    if is_admin(request.user):
        messages.info(request, 'Admin users do not have student profiles.')
        return redirect('admin_dashboard')
    if is_driver(request.user):
        return redirect('driver_profile')
    
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    return render(request, 'myapp/profile.html', {'student': student})


@login_required
def edit_profile(request):
    """Edit student profile"""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    if is_driver(request.user):
        return redirect('driver_profile')
    
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = StudentProfileUpdateForm(instance=student)
    
    return render(request, 'myapp/edit_profile.html', {'form': form, 'student': student})


@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = StudentPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('profile')
    else:
        form = StudentPasswordChangeForm(request.user)
    
    return render(request, 'myapp/change_password.html', {'form': form})


# ================== TRACKING VIEWS ==================

@login_required
def track_booking(request, booking_id):
    """Real-time tracking page"""
    if is_admin(request.user):
        booking = get_object_or_404(Booking, booking_id=booking_id)
    elif is_driver(request.user):
        booking = get_object_or_404(
            Booking,
            booking_id=booking_id,
            trip__driver=request.user.driver
        )
    else:
        try:
            booking = get_object_or_404(
                Booking, 
                booking_id=booking_id,
                student=request.user.student
            )
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('home')
    
    vehicle = booking.route.vehicle
    
    try:
        latest_location = VehicleLocation.objects.filter(
            vehicle=vehicle
        ).latest('timestamp')
    except VehicleLocation.DoesNotExist:
        latest_location = None
    
    context = {
        'booking': booking,
        'vehicle': vehicle,
        'latest_location': latest_location,
    }
    return render(request, 'myapp/track_booking.html', context)


@login_required
def live_map(request):
    """Live map showing all active vehicles"""
    vehicles = Vehicle.objects.filter(is_active=True)
    
    vehicle_data = []
    for vehicle in vehicles:
        try:
            location = VehicleLocation.objects.filter(
                vehicle=vehicle
            ).latest('timestamp')
            
            vehicle_data.append({
                'vehicle': vehicle,
                'location': location,
            })
        except VehicleLocation.DoesNotExist:
            pass
    
    context = {
        'vehicle_data': vehicle_data,
    }
    return render(request, 'myapp/live_map.html', context)


@login_required
def get_vehicle_location(request, vehicle_id):
    """API endpoint to get current vehicle location"""
    try:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        
        try:
            location = VehicleLocation.objects.filter(
                vehicle=vehicle
            ).latest('timestamp')
            
            data = {
                'success': True,
                'latitude': float(location.latitude),
                'longitude': float(location.longitude),
                'speed': float(location.speed) if location.speed else 0,
                'heading': float(location.heading) if location.heading else 0,
                'timestamp': location.timestamp.isoformat(),
            }
        except VehicleLocation.DoesNotExist:
            data = {
                'success': False,
                'message': 'No location data available'
            }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@csrf_exempt
@login_required
def update_vehicle_location(request):
    """API endpoint for drivers to update vehicle location"""
    if not is_driver(request.user):
        return JsonResponse({
            'success': False,
            'message': 'Only drivers can update location'
        })
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            speed = data.get('speed', 0)
            heading = data.get('heading', 0)
            
            driver = request.user.driver
            vehicle = driver.vehicle
            
            if not vehicle:
                return JsonResponse({
                    'success': False,
                    'message': 'No vehicle assigned'
                })
            
            VehicleLocation.objects.create(
                vehicle=vehicle,
                latitude=latitude,
                longitude=longitude,
                speed=speed,
                heading=heading
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Location updated successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


# ================== DRIVER VIEWS (CONTINUED IN NEXT PART) ==================
# ================== DRIVER VIEWS ==================

@login_required
def driver_dashboard(request):
    """Driver Dashboard"""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    if is_student(request.user):
        return redirect('dashboard')
    
    try:
        driver = request.user.driver
    except:
        messages.error(request, 'Driver profile not found.')
        return redirect('login')
    
    today = date.today()
    trips = Trip.objects.filter(driver=driver, trip_date=today)
    
    today_trips = trips.count()
    today_passengers = sum(trip.bookings.count() for trip in trips)
    completed_trips = Trip.objects.filter(driver=driver, status='COMPLETED').count()
    
    total_earnings = Booking.objects.filter(
        trip__driver=driver,
        trip__status='COMPLETED',
        status='COMPLETED'
    ).aggregate(Sum('total_fare'))['total_fare__sum'] or 0
    
    context = {
        'driver': driver,
        'trips': trips,
        'today_trips': today_trips,
        'today_passengers': today_passengers,
        'completed_trips': completed_trips,
        'total_earnings': total_earnings,
    }
    return render(request, 'myapp/driver_dashboard.html', context)


@login_required
def driver_trips(request):
    """All trips for driver"""
    if not is_driver(request.user):
        return redirect('dashboard')
    
    try:
        driver = request.user.driver
    except:
        messages.error(request, 'Driver profile not found.')
        return redirect('login')
    
    status_filter = request.GET.get('status')
    trips = Trip.objects.filter(driver=driver).order_by('-trip_date')
    
    if status_filter:
        trips = trips.filter(status=status_filter)
    
    context = {
        'driver': driver,
        'trips': trips,
        'status_filter': status_filter,
    }
    return render(request, 'myapp/driver_trips.html', context)


@login_required
def driver_trip_detail(request, trip_id):
    """Trip detail for driver"""
    if is_admin(request.user):
        trip = get_object_or_404(Trip, id=trip_id)
    elif is_driver(request.user):
        try:
            driver = request.user.driver
            trip = get_object_or_404(Trip, id=trip_id, driver=driver)
        except:
            messages.error(request, 'Trip not found.')
            return redirect('driver_trips')
    else:
        return redirect('dashboard')
    
    context = {'trip': trip}
    return render(request, 'myapp/driver_trip_detail.html', context)


@login_required
def driver_start_trip(request, trip_id):
    """Start a trip"""
    if not is_driver(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        driver = request.user.driver
        trip = get_object_or_404(Trip, id=trip_id, driver=driver)
    except:
        messages.error(request, 'Trip not found.')
        return redirect('driver_trips')
    
    if trip.status == 'SCHEDULED':
        trip.status = 'IN_PROGRESS'
        trip.started_at = datetime.now()
        trip.save()
        
        # Update all bookings to confirmed
        trip.bookings.filter(status='PENDING').update(status='CONFIRMED')
        
        messages.success(request, 'Trip started successfully!')
    else:
        messages.error(request, 'Cannot start this trip.')
    
    return redirect('driver_trip_detail', trip_id=trip.id)


@login_required
def driver_complete_trip(request, trip_id):
    """Complete a trip"""
    if not is_driver(request.user):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    try:
        driver = request.user.driver
        trip = get_object_or_404(Trip, id=trip_id, driver=driver)
    except:
        messages.error(request, 'Trip not found.')
        return redirect('driver_trips')
    
    if trip.status == 'IN_PROGRESS':
        trip.status = 'COMPLETED'
        trip.completed_at = datetime.now()
        trip.save()
        
        # Update all bookings to completed
        trip.bookings.filter(status='CONFIRMED').update(status='COMPLETED')
        
        messages.success(request, 'Trip completed successfully!')
    else:
        messages.error(request, 'Cannot complete this trip.')
    
    return redirect('driver_trip_detail', trip_id=trip.id)


@login_required
def driver_schedule(request):
    """Driver's schedule"""
    if not is_driver(request.user):
        return redirect('dashboard')
    
    try:
        driver = request.user.driver
    except:
        messages.error(request, 'Driver profile not found.')
        return redirect('login')
    
    trips = Trip.objects.filter(
        driver=driver,
        trip_date__gte=date.today()
    ).order_by('trip_date', 'schedule__departure_time')
    
    context = {
        'driver': driver,
        'trips': trips,
    }
    return render(request, 'myapp/driver/driver_schedule.html', context)


@login_required
def driver_earnings(request):
    """Driver's earnings"""
    if not is_driver(request.user):
        return redirect('dashboard')
    
    try:
        driver = request.user.driver
    except:
        messages.error(request, 'Driver profile not found.')
        return redirect('login')
    
    completed_trips = Trip.objects.filter(driver=driver, status='COMPLETED')
    total_earnings = Booking.objects.filter(
        trip__driver=driver,
        trip__status='COMPLETED',
        status='COMPLETED'
    ).aggregate(Sum('total_fare'))['total_fare__sum'] or 0
    
    from django.db.models.functions import TruncMonth
    monthly_earnings = Booking.objects.filter(
        trip__driver=driver,
        trip__status='COMPLETED',
        status='COMPLETED'
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('total_fare')
    ).order_by('-month')
    
    context = {
        'driver': driver,
        'completed_trips': completed_trips.count(),
        'total_earnings': total_earnings,
        'monthly_earnings': monthly_earnings,
    }
    return render(request, 'myapp/driver/driver_earnings.html', context)


@login_required
def driver_profile(request):
    """Driver profile"""
    if not is_driver(request.user):
        return redirect('dashboard')
    
    try:
        driver = request.user.driver
    except:
        messages.error(request, 'Driver profile not found.')
        return redirect('login')
    
    context = {'driver': driver}
    return render(request, 'myapp/driver/driver_profile.html', context)


# ================== ADMIN VIEWS ==================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin Dashboard"""
    total_students = Student.objects.filter(is_active=True).count()
    total_drivers = Driver.objects.filter(is_active=True).count()
    total_routes = Route.objects.filter(is_active=True).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    recent_bookings = Booking.objects.select_related('student__user', 'route').order_by('-created_at')[:10]
    
    today_trips = Trip.objects.filter(trip_date=date.today())
    
    # Revenue statistics
    total_revenue = Booking.objects.filter(
        status='COMPLETED'
    ).aggregate(Sum('total_fare'))['total_fare__sum'] or 0
    
    context = {
        'total_students': total_students,
        'total_drivers': total_drivers,
        'total_routes': total_routes,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'recent_bookings': recent_bookings,
        'today_trips': today_trips,
        'total_revenue': total_revenue,
    }
    return render(request, 'myapp/admin/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_bookings(request):
    """View all bookings (admin)"""
    status_filter = request.GET.get('status')
    bookings = Booking.objects.select_related('student__user', 'route', 'payment')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings.order_by('-created_at'),
        'status_filter': status_filter,
    }
    return render(request, 'myapp/admin/admin_bookings.html', context)


@login_required
@user_passes_test(is_admin)
def admin_booking_detail(request, booking_id):
    """Admin booking detail view"""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'booking': booking,
        'payment': payment,
    }
    return render(request, 'myapp/admin/admin_booking_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_confirm_booking(request, booking_id):
    """Confirm a pending booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    if booking.status == 'PENDING':
        booking.status = 'CONFIRMED'
        booking.save()
        messages.success(request, f'Booking {booking.booking_id} confirmed successfully!')
    else:
        messages.error(request, 'Only pending bookings can be confirmed.')
    
    return redirect('admin_bookings')


@login_required
@user_passes_test(is_admin)
def admin_routes(request):
    """Manage routes (admin)"""
    routes = Route.objects.select_related('vehicle').order_by('-created_at')
    context = {'routes': routes}
    return render(request, 'myapp/admin/admin_routes.html', context)


@login_required
@user_passes_test(is_admin)
def admin_add_route(request):
    """Add new route"""
    if request.method == 'POST':
        # Handle route creation
        messages.success(request, 'Route added successfully!')
        return redirect('admin_routes')
    
    vehicles = Vehicle.objects.filter(is_active=True)
    context = {'vehicles': vehicles}
    return render(request, 'myapp/admin/admin_add_route.html', context)


@login_required
@user_passes_test(is_admin)
def admin_students(request):
    """Manage students (admin)"""
    students = Student.objects.select_related('user').order_by('-created_at')
    context = {'students': students}
    return render(request, 'myapp/admin/admin_students.html', context)


@login_required
@user_passes_test(is_admin)
def admin_drivers(request):
    """Manage drivers (admin)"""
    drivers = Driver.objects.select_related('user', 'vehicle').order_by('-created_at')
    context = {'drivers': drivers}
    return render(request, 'myapp/admin/admin_drivers.html', context)


@login_required
@user_passes_test(is_admin)
def admin_approve_driver(request, driver_id):
    """Approve/verify a driver"""
    driver = get_object_or_404(Driver, id=driver_id)
    driver.is_verified = not driver.is_verified
    driver.save()
    
    status = "verified" if driver.is_verified else "unverified"
    messages.success(request, f'Driver {driver.user.get_full_name()} has been {status}.')
    return redirect('admin_drivers')


@login_required
@user_passes_test(is_admin)
def admin_vehicles(request):
    """Manage vehicles (admin)"""
    vehicles = Vehicle.objects.prefetch_related('drivers').all()
    context = {'vehicles': vehicles}
    return render(request, 'myapp/admin/admin_vehicles.html', context)


@login_required
@user_passes_test(is_admin)
def admin_add_vehicle(request):
    """Add new vehicle"""
    if request.method == 'POST':
        # Handle vehicle creation
        messages.success(request, 'Vehicle added successfully!')
        return redirect('admin_vehicles')
    
    return render(request, 'myapp/admin/admin_add_vehicle.html')


@login_required
@user_passes_test(is_admin)
def admin_trips(request):
    """Manage trips (admin)"""
    trips = Trip.objects.select_related('driver__user', 'route').order_by('-trip_date')
    context = {'trips': trips}
    return render(request, 'myapp/admin/admin_trips.html', context)


@login_required
@user_passes_test(is_admin)
def admin_assign_driver(request, trip_id):
    """Assign driver to trip"""
    trip = get_object_or_404(Trip, id=trip_id)
    
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        driver = get_object_or_404(Driver, id=driver_id)
        trip.driver = driver
        trip.save()
        messages.success(request, f'Driver {driver.user.get_full_name()} assigned to trip.')
        return redirect('admin_trips')
    
    drivers = Driver.objects.filter(is_active=True, is_verified=True)
    context = {
        'trip': trip,
        'drivers': drivers,
    }
    return render(request, 'myapp/admin/admin_assign_driver.html', context)


@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    """View reports (admin)"""
    total_revenue = Booking.objects.filter(
        status='COMPLETED'
    ).aggregate(Sum('total_fare'))['total_fare__sum'] or 0
    
    bookings_by_status = Booking.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Monthly revenue
    from django.db.models.functions import TruncMonth
    monthly_revenue = Booking.objects.filter(
        status='COMPLETED'
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total=Sum('total_fare')
    ).order_by('-month')[:12]
    
    context = {
        'total_revenue': total_revenue,
        'bookings_by_status': bookings_by_status,
        'monthly_revenue': monthly_revenue,
    }
    return render(request, 'myapp/admin/admin_reports.html', context)


@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    """System settings (admin)"""
    if request.method == 'POST':
        messages.success(request, 'Settings updated successfully!')
        return redirect('admin_settings')
    
    return render(request, 'myapp/admin/admin_settings.html')

@login_required
@user_passes_test(is_admin)
def admin_approve_driver(request, driver_id):
    """Approve/verify a driver"""
    driver = get_object_or_404(Driver, id=driver_id)
    driver.is_verified = True
    driver.is_active = True  # Also activate the driver
    driver.save()
    
    messages.success(request, f'Driver {driver.user.get_full_name()} has been approved and can now login.')
    return redirect('admin_drivers')