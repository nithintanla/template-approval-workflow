from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dashboard.models import Brand, Template, Agent, Analytics
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

        # Create test templates with different statuses
        templates = []
        statuses = ['draft', 'pending', 'approved', 'rejected']
        messages = [
            'Welcome to our Good service!',
            'Sorry for the Bad experience',
            'Check out our latest offers!'
        ]
        
        for brand in brands:
            for msg in messages:
                template, _ = Template.objects.get_or_create(
                    title=f'Template - {msg[:20]}',
                    content=msg,
                    message_type=random.choice(['text', 'media', 'card']),
                    status=random.choice(statuses),
                    brand=brand,
                    created_by=user
                )
                templates.append(template)

        # Create test analytics
        for template in templates:
            for i in range(7):  # Last 7 days of data
                Analytics.objects.get_or_create(
                    template=template,
                    views=random.randint(100, 1000),
                    responses=random.randint(10, 100),
                    date=datetime.now().date() - timedelta(days=i)
                )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
