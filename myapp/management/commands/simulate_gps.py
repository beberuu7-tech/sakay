from django.core.management.base import BaseCommand
from myapp.models import Vehicle, VehicleLocation
from decimal import Decimal
import time
import random

class Command(BaseCommand):
    help = 'Simulates GPS updates for testing'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Starting GPS simulation...')
        
        vehicles = Vehicle.objects.filter(is_active=True)
        
        if not vehicles.exists():
            self.stdout.write(self.style.ERROR('No active vehicles!'))
            return
        
        positions = {}
        for vehicle in vehicles:
            positions[vehicle.id] = {
                'lat': Decimal('11.6000') + Decimal(str(random.uniform(-0.05, 0.05))),
                'lng': Decimal('124.4000') + Decimal(str(random.uniform(-0.05, 0.05))),
                'speed': Decimal(str(random.uniform(20, 60)))
            }
        
        try:
            iteration = 1
            while True:
                for vehicle in vehicles:
                    pos = positions[vehicle.id]
                    
                    pos['lat'] += Decimal(str(random.uniform(-0.001, 0.001)))
                    pos['lng'] += Decimal(str(random.uniform(-0.001, 0.001)))
                    pos['speed'] = max(Decimal('0'), min(Decimal('80'), 
                                    pos['speed'] + Decimal(str(random.uniform(-5, 5)))))
                    
                    VehicleLocation.objects.create(
                        vehicle=vehicle,
                        latitude=pos['lat'],
                        longitude=pos['lng'],
                        speed=pos['speed'],
                        heading=Decimal(str(random.uniform(0, 360)))
                    )
                    
                    self.stdout.write(
                        f"[{iteration}] {vehicle.plate_number}: "
                        f"Lat {pos['lat']:.6f}, Lng {pos['lng']:.6f}, "
                        f"Speed {pos['speed']:.1f} km/h"
                    )
                
                iteration += 1
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('\nGPS simulation stopped.'))