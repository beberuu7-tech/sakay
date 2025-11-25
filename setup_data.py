# setup_data.py - Run this script to create sample data
# Place in your project root and run: python manage.py shell < setup_data.py

from django.contrib.auth.models import User
from sakay.models import *
from datetime import date, timedelta
import random

print("🚀 Starting Sakay System Setup...")
print("=" * 50)

# 1. Create or get admin user
print("\n1️⃣ Setting up Admin user...")
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@sakay.ph',
        'first_name': 'System',
        'last_name': 'Administrator',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("   ✅ Admin user created: admin / admin123")
else:
    print("   ℹ️  Admin user already exists")

# 2. Create Vehicle
print("\n2️⃣ Setting up Vehicle...")
vehicle, created = Vehicle.objects.get_or_create(
    plate_number='ABC-1234',
    defaults={
        'vehicle_type': 'VAN',
        'model': 'Toyota Hiace',
        'color': 'White',
        'capacity': 15,
        'year': 2020,
        'is_active': True
    }
)
if created:
    print(f"   ✅ Vehicle created: {vehicle.plate_number}")
else:
    print(f"   ℹ️  Vehicle already exists: {vehicle.plate_number}")

# 3. Create Driver
print("\n3️⃣ Setting up Driver user...")
driver_user, created = User.objects.get_or_create(
    username='driver1',
    defaults={
        'email': 'driver@sakay.ph',
        'first_name': 'Juan',
        'last_name': 'Cruz',
    }
)
if created:
    driver_user.set_password('driver123')
    driver_user.save()
    print("   ✅ Driver user created: driver1 / driver123")
else:
    print("   ℹ️  Driver user already exists")

driver, created = Driver.objects.get_or_create(
    user=driver_user,
    defaults={
        'driver_id': 'DRV2025001',
        'license_number': 'N01-12-345678',
        'license_expiry': date(2026, 12, 31),
        'phone_number': '+639171234567',
        'address': 'Naval, Biliran',
        'date_of_birth': date(1985, 5, 15),
        'emergency_contact_name': 'Maria Cruz',
        'emergency_contact_number': '+639181234567',
        'vehicle': vehicle,
        'is_active': True,
        'is_verified': True
    }
)
if created:
    print(f"   ✅ Driver profile created: {driver.driver_id}")
else:
    print(f"   ℹ️  Driver profile already exists: {driver.driver_id}")

# 4. Create Sample Student
print("\n4️⃣ Setting up Sample Student...")
student_user, created = User.objects.get_or_create(
    username='student1',
    defaults={
        'email': 'student@gmail.com',
        'first_name': 'Pedro',
        'last_name': 'Santos',
    }
)
if created:
    student_user.set_password('student123')
    student_user.save()
    print("   ✅ Student user created: student1 / student123")
else:
    print("   ℹ️  Student user already exists")

student, created = Student.objects.get_or_create(
    user=student_user,
    defaults={
        'student_id': 'ST2025001',
        'phone_number': '+639281234567',
        'address': 'Culaba, Biliran',
        'date_of_birth': date(2005, 8, 20),
        'guardian_name': 'Rosa Santos',
        'guardian_relationship': 'PARENT',
        'guardian_contact': '+639291234567',
        'emergency_contact_name': 'Rosa Santos',
        'emergency_contact_relationship': 'PARENT',
        'emergency_contact_number': '+639291234567',
        'is_active': True
    }
)
if created:
    print(f"   ✅ Student profile created: {student.student_id}")
else:
    print(f"   ℹ️  Student profile already exists: {student.student_id}")

# 5. Create Route
print("\n5️⃣ Setting up Route...")
route, created = Route.objects.get_or_create(
    route_code='RT001',
    defaults={
        'route_name': 'Culaba to Naval',
        'origin': 'Culaba',
        'destination': 'Naval',
        'distance_km': 25.5,
        'fare': 50.00,
        'estimated_duration': '45 minutes',
        'route_type': 'PICKUP',
        'vehicle': vehicle,
        'is_active': True
    }
)
if created:
    print(f"   ✅ Route created: {route.route_code}")
else:
    print(f"   ℹ️  Route already exists: {route.route_code}")

# 6. Create Stops
print("\n6️⃣ Setting up Stops...")
stops_data = [
    {'stop_name': 'Culaba Terminal', 'stop_order': 1, 'estimated_arrival_time': '06:00:00'},
    {'stop_name': 'Kawayan Junction', 'stop_order': 2, 'estimated_arrival_time': '06:20:00'},
    {'stop_name': 'Almeria Town Center', 'stop_order': 3, 'estimated_arrival_time': '06:35:00'},
    {'stop_name': 'Naval Public Market', 'stop_order': 4, 'estimated_arrival_time': '06:50:00'},
]

for stop_data in stops_data:
    stop, created = Stop.objects.get_or_create(
        route=route,
        stop_order=stop_data['stop_order'],
        defaults={
            'stop_name': stop_data['stop_name'],
            'estimated_arrival_time': stop_data['estimated_arrival_time']
        }
    )
    if created:
        print(f"   ✅ Stop created: {stop.stop_name}")

# 7. Create Schedule
print("\n7️⃣ Setting up Schedule...")
schedule, created = Schedule.objects.get_or_create(
    route=route,
    day_of_week='MONDAY',
    defaults={
        'departure_time': '06:00:00',
        'arrival_time': '06:50:00',
        'is_active': True
    }
)
if created:
    print(f"   ✅ Schedule created: {schedule.day_of_week} {schedule.departure_time}")
else:
    print(f"   ℹ️  Schedule already exists")

# 8. Create Trip for today
print("\n8️⃣ Setting up Today's Trip...")
today = date.today()
trip, created = Trip.objects.get_or_create(
    route=route,
    schedule=schedule,
    trip_date=today,
    defaults={
        'driver': driver,
        'status': 'SCHEDULED'
    }
)
if created:
    print(f"   ✅ Trip created for {today}")
else:
    print(f"   ℹ️  Trip already exists for {today}")

# 9. Create Sample Booking
print("\n9️⃣ Setting up Sample Booking...")
pickup_stop = Stop.objects.filter(route=route).first()
dropoff_stop = Stop.objects.filter(route=route).last()

booking, created = Booking.objects.get_or_create(
    student=student,
    route=route,
    booking_date=today,
    defaults={
        'schedule': schedule,
        'trip': trip,
        'pickup_stop': pickup_stop,
        'dropoff_stop': dropoff_stop,
        'seats_booked': 1,
        'total_fare': route.fare,
        'status': 'CONFIRMED'
    }
)
if created:
    print(f"   ✅ Booking created: {booking.booking_id}")
    
    # Create payment
    Payment.objects.create(
        booking=booking,
        amount=booking.total_fare,
        payment_method='CASH',
        payment_status='PENDING'
    )
    print(f"   ✅ Payment record created")
else:
    print(f"   ℹ️  Booking already exists: {booking.booking_id}")

# 10. Create Sample GPS Location
print("\n🔟 Setting up GPS Location...")
location, created = VehicleLocation.objects.get_or_create(
    vehicle=vehicle,
    latitude=11.6000,
    longitude=124.4000,
    defaults={
        'speed': 45.0,
        'heading': 90.0
    }
)
if created:
    print(f"   ✅ GPS location created")
else:
    print(f"   ℹ️  GPS location already exists")

print("\n" + "=" * 50)
print("✅ Setup Complete!")
print("\n📋 Login Credentials:")
print("   Admin:   username='admin'    password='admin123'")
print("   Driver:  username='driver1'  password='driver123'")
print("   Student: username='student1' password='student123'")
print("\n🚀 Next Steps:")
print("   1. Run GPS simulation: python manage.py simulate_gps")
print("   2. Start server: python manage.py runserver")
print("   3. Test all three dashboards!")
print("=" * 50)