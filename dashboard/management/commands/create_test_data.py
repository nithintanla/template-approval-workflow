from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Brand, Agent
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Creates test data for the RBM Portal'

    def handle(self, *args, **kwargs):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_staff': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Create test brands
        brands = []
        for i in range(1, 4):
            brand, _ = Brand.objects.get_or_create(
                name=f'Test Brand {i}',
                description=f'Test Brand {i} Description'
            )
            brands.append(brand)

        # Create test agents
        for brand in brands:
            for i in range(1, 4):
                Agent.objects.get_or_create(
                    name=f'Agent {i} - {brand.name}',
                    email=f'agent{i}@{brand.name.lower().replace(" ", "")}.com',
                    brand=brand
                )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
