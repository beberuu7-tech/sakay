# myapp/management/commands/populate_biliran_routes.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Driver, Vehicle, Route, Stop, Schedule
from datetime import time, timedelta, date
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates Biliran Province routes with various vehicle types'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚍 Creating Biliran Province Transportation Routes...')
        
        # Create Drivers
        drivers = self.create_drivers()
        
        # Create Vehicles (Various Types)
        vehicles = self.create_vehicles(drivers)
        
        # Create Routes
        self.create_naval_to_almeria_route(vehicles['van1'])
        self.create_naval_to_kawayan_route(vehicles['bus1'])
        self.create_naval_to_culaba_route(vehicles['van2'])
        self.create_almeria_circuit_route(vehicles['jeepney1'])
        self.create_kawayan_circuit_route(vehicles['bus2'])
        self.create_culaba_circuit_route(vehicles['van3'])
        # tricycle mapped to an existing vehicle type choice (using JEEPNEY here to avoid invalid choice)
        self.create_naval_tricycle_routes(vehicles['jeepney2'])
        self.create_campus_shuttle_route(vehicles['coaster1'])
        
        self.stdout.write(self.style.SUCCESS('✅ Successfully created all Biliran routes!'))

    def create_drivers(self):
        """Create sample drivers"""
        drivers = {}
        
        driver_data = [
            ('driver1', 'Juan', 'Dela Cruz', 'DRV-001'),
            ('driver2', 'Pedro', 'Santos', 'DRV-002'),
            ('driver3', 'Maria', 'Garcia', 'DRV-003'),
            ('driver4', 'Jose', 'Reyes', 'DRV-004'),
            ('driver5', 'Ana', 'Lopez', 'DRV-005'),
            ('driver6', 'Carlos', 'Martinez', 'DRV-006'),
            ('driver7', 'Rosa', 'Fernandez', 'DRV-007'),
            ('driver8', 'Miguel', 'Torres', 'DRV-008'),
        ]
        
        for username, first, last, driver_id in driver_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{username}@biliran.ph'
                }
            )
            if created:
                user.set_password('driver123')
                user.save()
            
            driver, created = Driver.objects.get_or_create(
                user=user,
                defaults={
                    'driver_id': driver_id,
                    'license_number': f'N01-{driver_id[-3:]}-456789',
                    'license_expiry': date(2026, 12, 31),
                    'phone_number': f'+63917{driver_id[-3:]}1234',
                    'address': 'Naval, Biliran',
                    'date_of_birth': date(1985, 1, 1),
                    'emergency_contact_name': f'{first} Emergency',
                    'emergency_contact_number': f'+63917{driver_id[-3:]}5678',
                    'is_active': True,
                    'is_verified': True
                }
            )
            drivers[username] = driver
        
        return drivers

    def create_vehicles(self, drivers):
        """Create various types of vehicles"""
        vehicles = {}
        
        # Vans
        vehicles['van1'] = self.create_vehicle('VAN', 'ABC 1234', 15, 'Toyota Hiace', 2020, 'White', drivers['driver1'])
        vehicles['van2'] = self.create_vehicle('VAN', 'DEF 5678', 12, 'Nissan Urvan', 2019, 'Silver', drivers['driver2'])
        vehicles['van3'] = self.create_vehicle('VAN', 'GHI 9012', 15, 'Toyota Hiace', 2021, 'Blue', drivers['driver3'])
        
        # Buses
        vehicles['bus1'] = self.create_vehicle('BUS', 'JKL 3456', 30, 'Isuzu Bus', 2019, 'White/Blue', drivers['driver4'])
        vehicles['bus2'] = self.create_vehicle('BUS', 'MNO 7890', 35, 'Hino Bus', 2020, 'White/Red', drivers['driver5'])
        
        # Jeepneys
        vehicles['jeepney1'] = self.create_vehicle('JEEPNEY', 'PQR 2345', 18, 'Traditional Jeepney', 2018, 'Colorful', drivers['driver6'])
        # create an extra jeepney to use for tricycle-style short routes (keeps choices valid)
        vehicles['jeepney2'] = self.create_vehicle('JEEPNEY', 'STU 6789', 4, 'Small Jeepney', 2020, 'Yellow', drivers['driver7'])
        
        # Coaster
        vehicles['coaster1'] = self.create_vehicle('COASTER', 'VWX 0123', 25, 'Toyota Coaster', 2021, 'White', drivers['driver8'])
        
        return vehicles

    def create_vehicle(self, vehicle_type, plate, capacity, model_name, year, color, driver):
        """Helper to create a vehicle"""
        vehicle, created = Vehicle.objects.get_or_create(
            plate_number=plate,
            defaults={
                'vehicle_type': vehicle_type,
                'model': model_name,
                'color': color,
                'capacity': capacity,
                'year': year,
                'is_active': True
            }
        )
        # link vehicle to driver
        driver.vehicle = vehicle
        driver.save()
        return vehicle

    def create_naval_to_almeria_route(self, vehicle):
        """Naval to Almeria Route (Main Highway)"""
        route, created = Route.objects.get_or_create(
            route_code='NAV-ALM-001',
            defaults={
                'route_name': 'Naval to Almeria Express',
                'route_type': 'PICKUP',
                'origin': 'Naval Terminal',
                'destination': 'Almeria Town Center',
                'distance_km': Decimal('12.00'),
                'estimated_duration': '30 minutes',
                'vehicle': vehicle,
                'fare': Decimal('50.00'),
                'is_active': True
            }
        )
        
        if created:
            stops_data = [
                ('Naval Terminal', '06:00:00'),
                ('Naval Public Market', '06:05:00'),
                ('BPSU Main Campus', '06:10:00'),
                ('Capiñahan', '06:15:00'),
                ('Talustusan', '06:20:00'),
                ('Almeria Junction', '06:25:00'),
                ('Almeria Town Center', '06:30:00'),
            ]
            self.create_stops(route, stops_data)
            self.create_daily_schedules(route, ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00'])

    def create_naval_to_kawayan_route(self, vehicle):
        """Naval to Kawayan Route (North Route)"""
        route, created = Route.objects.get_or_create(
            route_code='NAV-KAW-001',
            defaults={
                'route_name': 'Naval to Kawayan via Caibiran',
                'route_type': 'PICKUP',
                'origin': 'Naval Terminal',
                'destination': 'Kawayan Town Proper',
                'distance_km': Decimal('25.00'),
                'estimated_duration': '1 hour',
                'vehicle': vehicle,
                'fare': Decimal('80.00'),
                'is_active': True
            }
        )
        
        if created:
            stops_data = [
                ('Naval Terminal', '06:00:00'),
                ('Caibiran Junction', '06:20:00'),
                ('Caibiran Town', '06:30:00'),
                ('Biliran-Kawayan Boundary', '06:45:00'),
                ('Kawayan Town Proper', '07:00:00'),
            ]
            self.create_stops(route, stops_data)
            self.create_daily_schedules(route, ['06:00', '09:00', '12:00', '15:00', '18:00'])

    def create_naval_to_culaba_route(self, vehicle):
        """Naval to Culaba Route (Circumferential)"""
        route, created = Route.objects.get_or_create(
            route_code='NAV-CUL-001',
            defaults={
                'route_name': 'Naval to Culaba Coastal Route',
                'route_type': 'PICKUP',
                'origin': 'Naval Terminal',
                'destination': 'Culaba Town Center',
                'distance_km': Decimal('30.00'),
                'estimated_duration': '1 hr 15 mins',
                'vehicle': vehicle,
                'fare': Decimal('90.00'),
                'is_active': True
            }
        )
        
        if created:
            stops_data = [
                ('Naval Terminal', '07:00:00'),
                ('Caraycaray', '07:15:00'),
                ('Cabucgayan', '07:30:00'),
                ('Caibiran via Coastal', '07:45:00'),
                ('Maripipi Junction', '08:00:00'),
                ('Culaba Town Center', '08:15:00'),
            ]
            self.create_stops(route, stops_data)
            self.create_daily_schedules(route, ['07:00', '10:00', '13:00', '16:00'])

    def create_almeria_circuit_route(self, vehicle):
        """Almeria Town Circuit (Jeepney Route)"""
        route, created = Route.objects.get_or_create(
            route_code='ALM-CIR-001',
            defaults={
                'route_name': 'Almeria Town Circuit',
                'route_type': 'ROUND',
                'origin': 'Almeria Town Center',
                'destination': 'Almeria Town Center',
                'distance_km': Decimal('20.00'),
                'estimated_duration': '1 hr 30 mins',
                'vehicle': vehicle,
                'fare': Decimal('40.00'),
                'is_active': True
            }
        )
        
        if created:
            barangays = [
                ('Almeria Town Center', '08:00:00'),
                ('Caucab', '08:10:00'),
                ('Iyosan', '08:20:00'),
                ('Jamorawon', '08:30:00'),
                ('Lo-ok', '08:40:00'),
                ('Matanga', '08:50:00'),
                ('Pili', '09:00:00'),
                ('Salangi', '09:10:00'),
                ('Tamarindo', '09:20:00'),
                ('Back to Town Center', '09:30:00'),
            ]
            self.create_stops(route, barangays)
            self.create_daily_schedules(route, ['08:00', '11:00', '14:00', '17:00'])

    def create_kawayan_circuit_route(self, vehicle):
        """Kawayan Town Circuit"""
        route, created = Route.objects.get_or_create(
            route_code='KAW-CIR-001',
            defaults={
                'route_name': 'Kawayan Barangay Tour',
                'route_type': 'ROUND',
                'origin': 'Kawayan Town Hall',
                'destination': 'Kawayan Town Hall',
                'distance_km': Decimal('35.00'),
                'estimated_duration': '2 hours',
                'vehicle': vehicle,
                'fare': Decimal('60.00'),
                'is_active': True
            }
        )
        
        if created:
            stops_data = [
                ('Kawayan Town Hall', '06:00:00'),
                ('Poblacion', '06:10:00'),
                ('Baganito', '06:20:00'),
                ('Balite', '06:30:00'),
                ('Mada-o', '06:45:00'),
                ('Mapuyo', '07:00:00'),
                ('San Lorenzo', '07:15:00'),
                ('Ungale', '07:30:00'),
                ('Villa Cornejo', '07:45:00'),
                ('Back to Town Hall', '08:00:00'),
            ]
            self.create_stops(route, stops_data)
            self.create_daily_schedules(route, ['06:00', '09:00', '13:00', '16:00'])

    def create_culaba_circuit_route(self, vehicle):
        """Culaba Town Circuit"""
        route, created = Route.objects.get_or_create(
            route_code='CUL-CIR-001',
            defaults={
                'route_name': 'Culaba Barangay Loop',
                'route_type': 'ROUND',
                'origin': 'Culaba Municipal Hall',
                'destination': 'Culaba Municipal Hall',
                'distance_km': Decimal('25.00'),
                'estimated_duration': '1 hr 45 mins',
                'vehicle': vehicle,
                'fare': Decimal('50.00'),
                'is_active': True
            }
        )
        
        if created:
            stops_data = [
                ('Culaba Municipal Hall', '08:00:00'),
                ('Acaban', '08:12:00'),
                ('Bacolod', '08:24:00'),
                ('Bool Central', '08:36:00'),
                ('Calipayan', '08:48:00'),
                ('Guindapunan', '09:00:00'),
                ('Looc', '09:15:00'),
                ('Marvel', '09:30:00'),
                ('Virginia', '09:40:00'),
                ('Back to Municipal Hall', '09:45:00'),
            ]
            self.create_stops(route, stops_data)
            self.create_daily_schedules(route, ['08:00', '11:00', '14:00', '17:00'])

    def create_naval_tricycle_routes(self, vehicle):
        """Naval Town Tricycle-like Routes (using a small jeepney/vehicle)"""
        route, created = Route.objects.get_or_create(
            route_code='NAV-TRI-001',
            defaults={
                'route_name': 'Naval Town Short Service',
                'route_type': 'ROUND',
                'origin': 'Naval Public Market',
                'destination': 'Naval Public Market',
                'distance_km': Decimal('5.00'),
                'estimated_duration': '20 minutes',
                'vehicle': vehicle,
                'fare': Decimal('15.00'),
                'is_active': True
            }
        )
        
        if created:
            stops_data = [
                ('Naval Public Market', '06:00:00'),
                ('Naval Town Hall', '06:05:00'),
                ('Naval Hospital', '06:10:00'),
                ('BPSU Main Gate', '06:15:00'),
                ('Back to Market', '06:20:00'),
            ]
            self.create_stops(route, stops_data)
            # Frequent schedules for short-service routes
            times = ['06:00', '06:30', '07:00', '07:30', '08:00', '08:30', '09:00', '09:30', 
                     '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']
            self.create_daily_schedules(route, times)

    def create_campus_shuttle_route(self, vehicle):
        """BPSU Campus Shuttle"""
        route, created = Route.objects.get_or_create(
            route_code='BPSU-SHUT-001',
            defaults={
                'route_name': 'BPSU Campus Shuttle',
                'route_type': 'ROUND',
                'origin': 'BPSU Main Gate',
                'destination': 'BPSU Main Gate',
                'distance_km': Decimal('15.00'),
                'estimated_duration': '40 minutes',
                'vehicle': vehicle,
                'fare': Decimal('20.00'),
                'is_active': True
            }
        )
        
        if created:
            stops_data = [
                ('BPSU Main Gate', '07:00:00'),
                ('Naval Terminal (Pick-up)', '07:05:00'),
                ('Naval Public Market', '07:10:00'),
                ('Capiñahan (Students)', '07:20:00'),
                ('BPSU Engineering Building', '07:30:00'),
                ('BPSU College of Education', '07:35:00'),
                ('BPSU Main Building', '07:40:00'),
            ]
            self.create_stops(route, stops_data)
            self.create_daily_schedules(route, ['07:00', '07:30', '12:00', '13:00', '17:00', '18:00'])

    def create_stops(self, route, stops_data):
        """Helper to create stops"""
        for idx, (name, arrival) in enumerate(stops_data, 1):
            # arrival can be a string like '06:00:00' which is acceptable for TimeField
            Stop.objects.create(
                route=route,
                stop_name=name,
                stop_order=idx,
                estimated_arrival_time=arrival
            )

    def create_daily_schedules(self, route, times):
        """Helper to create daily schedules"""
        days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
        for day in days:
            for time_str in times:
                hour, minute = map(int, time_str.split(':'))
                departure = time(hour, minute)
                # basic arrival: +1 hour (wraps automatically)
                arrival_hour = (hour + 1) % 24
                arrival = time(arrival_hour, minute)
                
                Schedule.objects.create(
                    route=route,
                    day_of_week=day,
                    departure_time=departure,
                    arrival_time=arrival,
                    is_active=True
                )

