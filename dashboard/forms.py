from django import forms
from .models import Template, Brand, Agent

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['title', 'content', 'variables', 'message_type', 'brand']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message_type'].initial = 'text'
        self.fields['brand'].initial = Brand.objects.filter(name='Apple').first()

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'email', 'brand', 'is_active']
