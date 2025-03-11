from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('media', 'Media'),
        ('card', 'Card'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    variables = models.JSONField(default=dict, blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Agent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Analytics(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    responses = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Analytics"
