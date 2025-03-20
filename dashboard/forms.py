from django import forms
from django.core.validators import RegexValidator
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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter brand name',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter brand description',
                'rows': 4,
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Brand name must be at least 2 characters long.")
        if Brand.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("A brand with this name already exists.")
        return name

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'email', 'brand', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter agent name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter agent email',
                'required': True,
            }),
            'brand': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Agent.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An agent with this email already exists.")
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Agent name must be at least 2 characters long.")
        return name
