# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('VAN', 'Van'),
        ('BUS', 'Bus'),
        ('JEEPNEY', 'Jeepney'),
        ('COASTER', 'Coaster'),
    ]
    
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    capacity = models.IntegerField()
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.vehicle_type} - {self.plate_number}"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    driver_id = models.CharField(max_length=50, unique=True)
    license_photo = models.ImageField(upload_to='drivers/licenses/', null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=15)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='drivers')
    profile_picture = models.ImageField(upload_to='drivers/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.driver_id}"

class Student(models.Model):
    RELATIONSHIP_CHOICES = [
        ('PARENT', 'Parent'),
        ('GUARDIAN', 'Guardian'),
        ('RELATIVE', 'Relative'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    guardian_name = models.CharField(max_length=200)
    guardian_relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='PARENT')
    guardian_contact = models.CharField(max_length=15)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='PARENT')
    emergency_contact_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='students/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

class Route(models.Model):
    ROUTE_TYPE_CHOICES = [
        ('PICKUP', 'Pickup'),
        ('DROP', 'Drop-off'),
        ('ROUND', 'Round Trip'),
    ]
    
    route_code = models.CharField(max_length=20, unique=True)
    route_name = models.CharField(max_length=200)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_duration = models.CharField(max_length=50)
    route_type = models.CharField(max_length=20, choices=ROUTE_TYPE_CHOICES)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.route_code} - {self.route_name}"

class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=200)
    stop_order = models.IntegerField()
    estimated_arrival_time = models.TimeField()
    
    class Meta:
        ordering = ['route', 'stop_order']
        unique_together = ['route', 'stop_order']
    
    def __str__(self):
        return f"{self.route.route_code} - Stop {self.stop_order}: {self.stop_name}"

class Schedule(models.Model):
    DAY_CHOICES = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['route', 'day_of_week', 'departure_time']
    
    def __str__(self):
        return f"{self.route.route_code} - {self.day_of_week} {self.departure_time}"

class Trip(models.Model):
    """Represents an actual trip instance for a specific date"""
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    trip_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-trip_date', '-schedule__departure_time']
        unique_together = ['route', 'schedule', 'trip_date']
    
    def __str__(self):
        return f"{self.route.route_code} - {self.trip_date} - {self.driver.user.get_full_name()}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    
    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bookings')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    booking_date = models.DateField()
    pickup_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='pickup_bookings')
    dropoff_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name='dropoff_bookings')
    seats_booked = models.IntegerField(default=1)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"BK{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.student.user.get_full_name()}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('GCASH', 'GCash'),
        ('CARD', 'Card'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    payment_id = models.CharField(max_length=20, unique=True, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = f"PY{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.payment_id} - ₱{self.amount}"
    # Add to myapp/models.py

class VehicleLocation(models.Model):
    """Store GPS location history for vehicles"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # km/h
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # degrees
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['vehicle', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.timestamp}"