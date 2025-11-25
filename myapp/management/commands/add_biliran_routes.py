# Create this file: myapp/management/commands/add_biliran_routes.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Driver, Vehicle, Route, Stop, Schedule
from datetime import time, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Adds Biliran Province routes to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating Biliran Province routes...')
        
        # Create or get a default driver and vehicle
        driver_user, created = User.objects.get_or_create(
            username='driver_biliran',
            defaults={
                'first_name': 'Juan',
                'last_name': 'Dela Cruz',
                'email': 'driver@biliran.ph'
            }
        )
        if created:
            driver_user.set_password('driver123')
            driver_user.save()
        
        driver, created = Driver.objects.get_or_create(
            user=driver_user,
            defaults={
                'driver_id': 'DRV-BIL-001',
                'license_number': 'N01-23-456789',
                'license_expiry': '2026-12-31',
                'phone_number': '+639171234567',
                'address': 'Naval, Biliran',
                'emergency_contact_name': 'Maria Dela Cruz',
                'emergency_contact_number': '+639171234568',
                'is_available': True
            }
        )
        
        vehicle, created = Vehicle.objects.get_or_create(
            vehicle_number='VEH-BIL-001',
            defaults={
                'vehicle_type': 'VAN',
                'plate_number': 'ABC 1234',
                'capacity': 15,
                'model': 'Toyota Hiace',
                'year': 2020,
                'color': 'White',
                'registration_expiry': '2026-06-30',
                'insurance_expiry': '2026-06-30',
                'driver': driver,
                'is_active': True
            }
        )
        
        # Create second vehicle for multiple routes
        vehicle2, created = Vehicle.objects.get_or_create(
            vehicle_number='VEH-BIL-002',
            defaults={
                'vehicle_type': 'BUS',
                'plate_number': 'XYZ 5678',
                'capacity': 25,
                'model': 'Isuzu Bus',
                'year': 2019,
                'color': 'Blue',
                'registration_expiry': '2026-06-30',
                'insurance_expiry': '2026-06-30',
                'driver': driver,
                'is_active': True
            }
        )
        
        # Route 1: Almeria Circuit Route
        self.create_almeria_route(vehicle)
        
        # Route 2: Kawayan Circuit Route
        self.create_kawayan_route(vehicle2)
        
        # Route 3: Culaba Circuit Route
        self.create_culaba_route(vehicle)
        
        # Route 4: Inter-Municipality Route (Almeria to Kawayan)
        self.create_almeria_kawayan_route(vehicle2)
        
        # Route 5: Inter-Municipality Route (Kawayan to Culaba)
        self.create_kawayan_culaba_route(vehicle)
        
        self.stdout.write(self.style.SUCCESS('Successfully created Biliran Province routes!'))

    def create_almeria_route(self, vehicle):
        """Create Almeria Circuit Route with all 13 barangays"""
        route, created = Route.objects.get_or_create(
            route_code='ALMER-001',
            defaults={
                'route_name': 'Almeria Circuit - Full Tour',
                'route_type': 'ROUND',
                'origin': 'Poblacion, Almeria',
                'destination': 'Poblacion, Almeria',
                'origin_lat': Decimal('11.5833'),
                'origin_lng': Decimal('124.3833'),
                'destination_lat': Decimal('11.5833'),
                'destination_lng': Decimal('124.3833'),
                'distance_km': Decimal('35.00'),
                'estimated_duration': timedelta(hours=2, minutes=30),
                'vehicle': vehicle,
                'fare': Decimal('100.00'),
                'is_active': True
            }
        )
        
        if created:
            # Add all 13 barangays as stops
            barangays = [
                ('Poblacion', '07:00:00'),
                ('Caucab', '07:10:00'),
                ('Iyosan', '07:20:00'),
                ('Jamorawon', '07:30:00'),
                ('Lo-ok', '07:40:00'),
                ('Matanga', '07:50:00'),
                ('Pili', '08:00:00'),
                ('Pulang Bato', '08:10:00'),
                ('Salangi', '08:20:00'),
                ('Sampao', '08:30:00'),
                ('Tabunan', '08:40:00'),
                ('Talahid', '08:50:00'),
                ('Tamarindo', '09:00:00'),
            ]
            
            for idx, (barangay, arrival_time) in enumerate(barangays, 1):
                Stop.objects.create(
                    route=route,
                    stop_name=f'{barangay}, Almeria',
                    stop_order=idx,
                    latitude=Decimal('11.5833'),
                    longitude=Decimal('124.3833'),
                    estimated_arrival_time=arrival_time,
                    is_active=True
                )
            
            # Add schedules
            days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
            for day in days:
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=time(7, 0),
                    arrival_time=time(9, 30),
                    is_active=True
                )

    def create_kawayan_route(self, vehicle):
        """Create Kawayan Circuit Route with all 20 barangays"""
        route, created = Route.objects.get_or_create(
            route_code='KAWAYAN-001',
            defaults={
                'route_name': 'Kawayan Circuit - Complete Tour',
                'route_type': 'ROUND',
                'origin': 'Poblacion, Kawayan',
                'destination': 'Poblacion, Kawayan',
                'origin_lat': Decimal('11.7000'),
                'origin_lng': Decimal('124.4667'),
                'destination_lat': Decimal('11.7000'),
                'destination_lng': Decimal('124.4667'),
                'distance_km': Decimal('50.00'),
                'estimated_duration': timedelta(hours=3, minutes=30),
                'vehicle': vehicle,
                'fare': Decimal('120.00'),
                'is_active': True
            }
        )
        
        if created:
            # Add all 20 barangays as stops
            barangays = [
                ('Poblacion', '06:00:00'),
                ('Baganito', '06:12:00'),
                ('Balacson', '06:24:00'),
                ('Balite', '06:36:00'),
                ('Bilwang', '06:48:00'),
                ('Bulalacao', '07:00:00'),
                ('Burabod', '07:12:00'),
                ('Buyo', '07:24:00'),
                ('Inasuyan', '07:36:00'),
                ('Kansanok', '07:48:00'),
                ('Mada-o', '08:00:00'),
                ('Mapuyo', '08:12:00'),
                ('Masagaosao', '08:24:00'),
                ('Masagongsong', '08:36:00'),
                ('San Lorenzo', '08:48:00'),
                ('Tabunan North', '09:00:00'),
                ('Tubig-Ginoo', '09:12:00'),
                ('Tucdao', '09:24:00'),
                ('Ungale', '09:36:00'),
                ('Villa Cornejo', '09:48:00'),
            ]
            
            for idx, (barangay, arrival_time) in enumerate(barangays, 1):
                Stop.objects.create(
                    route=route,
                    stop_name=f'{barangay}, Kawayan',
                    stop_order=idx,
                    latitude=Decimal('11.7000'),
                    longitude=Decimal('124.4667'),
                    estimated_arrival_time=arrival_time,
                    is_active=True
                )
            
            # Add schedules
            days = ['MON', 'WED', 'FRI']
            for day in days:
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=time(6, 0),
                    arrival_time=time(9, 30),
                    is_active=True
                )

    def create_culaba_route(self, vehicle):
        """Create Culaba Circuit Route with all 17 barangays"""
        route, created = Route.objects.get_or_create(
            route_code='CULABA-001',
            defaults={
                'route_name': 'Culaba Circuit - Full Route',
                'route_type': 'ROUND',
                'origin': 'Culaba Central',
                'destination': 'Culaba Central',
                'origin_lat': Decimal('11.6167'),
                'origin_lng': Decimal('124.5333'),
                'destination_lat': Decimal('11.6167'),
                'destination_lng': Decimal('124.5333'),
                'distance_km': Decimal('40.00'),
                'estimated_duration': timedelta(hours=3, minutes=0),
                'vehicle': vehicle,
                'fare': Decimal('110.00'),
                'is_active': True
            }
        )
        
        if created:
            # Add all 17 barangays as stops
            barangays = [
                ('Culaba Central', '08:00:00'),
                ('Acaban', '08:12:00'),
                ('Bacolod', '08:24:00'),
                ('Binongtoan', '08:36:00'),
                ('Bool Central', '08:48:00'),
                ('Bool East', '09:00:00'),
                ('Bool West', '09:12:00'),
                ('Calipayan', '09:24:00'),
                ('Guindapunan', '09:36:00'),
                ('Habuhab', '09:48:00'),
                ('Looc', '10:00:00'),
                ('Marvel', '10:12:00'),
                ('Patag', '10:24:00'),
                ('Pinamihagan', '10:36:00'),
                ('Salvacion', '10:48:00'),
                ('San Roque', '11:00:00'),
                ('Virginia', '11:12:00'),
            ]
            
            for idx, (barangay, arrival_time) in enumerate(barangays, 1):
                Stop.objects.create(
                    route=route,
                    stop_name=f'{barangay}, Culaba',
                    stop_order=idx,
                    latitude=Decimal('11.6167'),
                    longitude=Decimal('124.5333'),
                    estimated_arrival_time=arrival_time,
                    is_active=True
                )
            
            # Add schedules
            days = ['TUE', 'THU', 'SAT']
            for day in days:
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=time(8, 0),
                    arrival_time=time(11, 0),
                    is_active=True
                )

    def create_almeria_kawayan_route(self, vehicle):
        """Create inter-municipality route from Almeria to Kawayan"""
        route, created = Route.objects.get_or_create(
            route_code='ALM-KAW-001',
            defaults={
                'route_name': 'Almeria to Kawayan Express',
                'route_type': 'PICKUP',
                'origin': 'Poblacion, Almeria',
                'destination': 'Poblacion, Kawayan',
                'origin_lat': Decimal('11.5833'),
                'origin_lng': Decimal('124.3833'),
                'destination_lat': Decimal('11.7000'),
                'destination_lng': Decimal('124.4667'),
                'distance_km': Decimal('18.00'),
                'estimated_duration': timedelta(hours=1, minutes=0),
                'vehicle': vehicle,
                'fare': Decimal('80.00'),
                'is_active': True
            }
        )
        
        if created:
            # Key stops between municipalities
            stops = [
                ('Poblacion, Almeria', '06:00:00'),
                ('Caucab, Almeria', '06:10:00'),
                ('Pili, Almeria', '06:20:00'),
                ('Tamarindo, Almeria', '06:30:00'),
                ('Baganito, Kawayan', '06:40:00'),
                ('Balite, Kawayan', '06:50:00'),
                ('Poblacion, Kawayan', '07:00:00'),
            ]
            
            for idx, (stop_name, arrival_time) in enumerate(stops, 1):
                Stop.objects.create(
                    route=route,
                    stop_name=stop_name,
                    stop_order=idx,
                    latitude=Decimal('11.6417'),
                    longitude=Decimal('124.4250'),
                    estimated_arrival_time=arrival_time,
                    is_active=True
                )
            
            # Daily morning and afternoon schedules
            for day in ['MON', 'TUE', 'WED', 'THU', 'FRI']:
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=time(6, 0),
                    arrival_time=time(7, 0),
                    is_active=True
                )
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=time(16, 0),
                    arrival_time=time(17, 0),
                    is_active=True
                )

    def create_kawayan_culaba_route(self, vehicle):
        """Create inter-municipality route from Kawayan to Culaba"""
        route, created = Route.objects.get_or_create(
            route_code='KAW-CUL-001',
            defaults={
                'route_name': 'Kawayan to Culaba Express',
                'route_type': 'PICKUP',
                'origin': 'Poblacion, Kawayan',
                'destination': 'Culaba Central',
                'origin_lat': Decimal('11.7000'),
                'origin_lng': Decimal('124.4667'),
                'destination_lat': Decimal('11.6167'),
                'destination_lng': Decimal('124.5333'),
                'distance_km': Decimal('15.00'),
                'estimated_duration': timedelta(minutes=50),
                'vehicle': vehicle,
                'fare': Decimal('70.00'),
                'is_active': True
            }
        )
        
        if created:
            # Key stops between municipalities
            stops = [
                ('Poblacion, Kawayan', '07:30:00'),
                ('Mapuyo, Kawayan', '07:40:00'),
                ('Ungale, Kawayan', '07:50:00'),
                ('Villa Cornejo, Kawayan', '08:00:00'),
                ('Acaban, Culaba', '08:10:00'),
                ('Bool Central, Culaba', '08:15:00'),
                ('Culaba Central', '08:20:00'),
            ]
            
            for idx, (stop_name, arrival_time) in enumerate(stops, 1):
                Stop.objects.create(
                    route=route,
                    stop_name=stop_name,
                    stop_order=idx,
                    latitude=Decimal('11.6584'),
                    longitude=Decimal('124.5000'),
                    estimated_arrival_time=arrival_time,
                    is_active=True
                )
            
            # Daily schedules
            for day in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']:
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=time(7, 30),
                    arrival_time=time(8, 20),
                    is_active=True
                )
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=time(15, 30),
                    arrival_time=time(16, 20),
                    is_active=True
                )