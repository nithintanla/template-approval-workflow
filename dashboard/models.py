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
        ('pending_l1', 'Pending L1 Approval'),
        ('approved_l1', 'Approved by L1'),
        ('rejected_l1', 'Rejected by L1'),
        ('approved_l2', 'Approved by L2'),
        ('rejected_l2', 'Rejected by L2'),
    ]

    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('media', 'Media'),
        ('card', 'Card'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    variables = models.TextField(blank=True)  # Allow any string without JSON validation
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_l1')
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

class ApprovalSettings(models.Model):
    rejection_keywords = models.TextField(
        help_text="Enter keywords separated by commas. Templates containing these words will be rejected."
    )
    keywords_approve = models.TextField(
        help_text="Enter keywords separated by commas. Templates containing these words will be approved automatically.",
        default=""
    )
    keywords_manual = models.TextField(
        help_text="Enter keywords separated by commas. Templates containing these words will be sent for manual approval.",
        default=""
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Approval Settings"
        verbose_name_plural = "Approval Settings"

    def get_keywords_list(self, field_name):
        return [k.strip().lower() for k in getattr(self, field_name).split(',') if k.strip()]
