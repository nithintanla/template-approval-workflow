from django import forms
from .models import Template, Brand, Agent

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['title', 'content', 'variables', 'message_type', 'brand']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'email', 'brand', 'is_active']
