from django import forms
from .models import Template, Brand, Agent

class TemplateForm(forms.ModelForm):
    # Make variables field optional with a custom widget
    variables = forms.JSONField(required=False, widget=forms.Textarea(attrs={
        'rows': 4,
        'placeholder': '{"variable_name": "default_value"}'
    }))

    class Meta:
        model = Template
        fields = ['title', 'content', 'variables', 'message_type', 'brand']

    def clean_variables(self):
        # Return empty dict if no variables provided
        variables = self.cleaned_data.get('variables')
        if not variables:
            return {}
        return variables

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['name', 'email', 'brand', 'is_active']
