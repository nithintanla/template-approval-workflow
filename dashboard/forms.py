from django import forms
from .models import Template

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
