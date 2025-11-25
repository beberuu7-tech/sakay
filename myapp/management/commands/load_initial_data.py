from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Vehicle, Route, Stop, Schedule
from datetime import time

class Command(BaseCommand):
    help = 'Load initial data only if database is empty'

    def handle(self, *args, **kwargs):
        # Check if data already exists
        if Route.objects.exists():
            self.stdout.write(self.style.WARNING('⚠ Data already exists. Skipping load.'))
            return

        self.stdout.write(self.style.SUCCESS('📦 Creating initial data...'))

        try:
            # Create Vehicles
            self.stdout.write('Creating vehicles...')
            vehicle1 = Vehicle.objects.create(
                plate_number='ABC123',
                vehicle_type='VAN',
                model='Toyota Hiace',
                color='White',
                capacity=15,
                year=2023,
                is_active=True
            )

            vehicle2 = Vehicle.objects.create(
                plate_number='XYZ789',
                vehicle_type='BUS',
                model='Mitsubishi Rosa',
                color='Blue',
                capacity=30,
                year=2022,
                is_active=True
            )

            vehicle3 = Vehicle.objects.create(
                plate_number='DEF456',
                vehicle_type='JEEPNEY',
                model='Modern Jeepney',
                color='Red',
                capacity=20,
                year=2023,
                is_active=True
            )

            vehicle4 = Vehicle.objects.create(
                plate_number='GHI789',
                vehicle_type='COASTER',
                model='Toyota Coaster',
                color='Silver',
                capacity=25,
                year=2024,
                is_active=True
            )

            self.stdout.write(self.style.SUCCESS('✓ Created 4 vehicles'))

            # Create Routes
            self.stdout.write('Creating routes...')
            
            # Route 1: Campus to City Center
            route1 = Route.objects.create(
                route_code='RT001',
                route_name='Campus to City Center',
                origin='University Campus',
                destination='City Center',
                distance_km=10.5,
                fare=50.00,
                estimated_duration='30 minutes',
                route_type='ROUND',
                vehicle=vehicle1,
                is_active=True
            )

            # Stops for Route 1
            Stop.objects.create(route=route1, stop_name='University Campus Gate', stop_order=1, estimated_arrival_time=time(7, 0))
            Stop.objects.create(route=route1, stop_name='Main Road Junction', stop_order=2, estimated_arrival_time=time(7, 10))
            Stop.objects.create(route=route1, stop_name='Shopping District', stop_order=3, estimated_arrival_time=time(7, 20))
            Stop.objects.create(route=route1, stop_name='City Center Plaza', stop_order=4, estimated_arrival_time=time(7, 30))

            # Schedules for Route 1
            for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']:
                Schedule.objects.create(
                    route=route1,
                    day_of_week=day,
                    departure_time=time(7, 0),
                    arrival_time=time(7, 30),
                    is_active=True
                )

            # Route 2: Mall to Residential Area
            route2 = Route.objects.create(
                route_code='RT002',
                route_name='Mall to Residential Area',
                origin='Shopping Mall',
                destination='Residential Complex',
                distance_km=8.0,
                fare=40.00,
                estimated_duration='25 minutes',
                route_type='ROUND',
                vehicle=vehicle2,
                is_active=True
            )

            # Stops for Route 2
            Stop.objects.create(route=route2, stop_name='Shopping Mall Entrance', stop_order=1, estimated_arrival_time=time(8, 0))
            Stop.objects.create(route=route2, stop_name='Market Street', stop_order=2, estimated_arrival_time=time(8, 10))
            Stop.objects.create(route=route2, stop_name='Park Avenue', stop_order=3, estimated_arrival_time=time(8, 15))
            Stop.objects.create(route=route2, stop_name='Residential Complex', stop_order=4, estimated_arrival_time=time(8, 25))

            # Schedules for Route 2
            for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']:
                Schedule.objects.create(
                    route=route2,
                    day_of_week=day,
                    departure_time=time(8, 0),
                    arrival_time=time(8, 25),
                    is_active=True
                )

            # Route 3: Downtown Express
            route3 = Route.objects.create(
                route_code='RT003',
                route_name='Downtown Express',
                origin='North Station',
                destination='South Terminal',
                distance_km=15.0,
                fare=60.00,
                estimated_duration='40 minutes',
                route_type='PICKUP',
                vehicle=vehicle3,
                is_active=True
            )

            # Stops for Route 3
            Stop.objects.create(route=route3, stop_name='North Station', stop_order=1, estimated_arrival_time=time(6, 30))
            Stop.objects.create(route=route3, stop_name='Downtown Center', stop_order=2, estimated_arrival_time=time(6, 50))
            Stop.objects.create(route=route3, stop_name='Business District', stop_order=3, estimated_arrival_time=time(7, 0))
            Stop.objects.create(route=route3, stop_name='South Terminal', stop_order=4, estimated_arrival_time=time(7, 10))

            # Schedules for Route 3
            for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']:
                Schedule.objects.create(
                    route=route3,
                    day_of_week=day,
                    departure_time=time(6, 30),
                    arrival_time=time(7, 10),
                    is_active=True
                )

            # Route 4: Coastal Highway
            route4 = Route.objects.create(
                route_code='RT004',
                route_name='Coastal Highway Route',
                origin='Beach Resort',
                destination='Harbor Port',
                distance_km=12.5,
                fare=55.00,
                estimated_duration='35 minutes',
                route_type='DROP',
                vehicle=vehicle4,
                is_active=True
            )

            # Stops for Route 4
            Stop.objects.create(route=route4, stop_name='Beach Resort', stop_order=1, estimated_arrival_time=time(9, 0))
            Stop.objects.create(route=route4, stop_name='Coastal Road', stop_order=2, estimated_arrival_time=time(9, 15))
            Stop.objects.create(route=route4, stop_name='Fisherman\'s Wharf', stop_order=3, estimated_arrival_time=time(9, 25))
            Stop.objects.create(route=route4, stop_name='Harbor Port', stop_order=4, estimated_arrival_time=time(9, 35))

            # Schedules for Route 4
            for day in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY']:
                Schedule.objects.create(
                    route=route4,
                    day_of_week=day,
                    departure_time=time(9, 0),
                    arrival_time=time(9, 35),
                    is_active=True
                )

            self.stdout.write(self.style.SUCCESS('✓ Created 4 routes with stops and schedules'))
            self.stdout.write(self.style.SUCCESS('✅ All initial data loaded successfully!'))
            self.stdout.write(self.style.SUCCESS(f'   - {Vehicle.objects.count()} vehicles'))
            self.stdout.write(self.style.SUCCESS(f'   - {Route.objects.count()} routes'))
            self.stdout.write(self.style.SUCCESS(f'   - {Stop.objects.count()} stops'))
            self.stdout.write(self.style.SUCCESS(f'   - {Schedule.objects.count()} schedules'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating data: {str(e)}'))
            # Don't raise - let build continue
            self.stdout.write(self.style.WARNING('⚠ Build will continue...'))