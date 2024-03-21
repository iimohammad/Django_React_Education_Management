from django import forms
from .models import AboutUs

class AboutUsForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = ['email', 'description', 'chancellor_name', 'chancellor_email', 'total_students', 'website_url']
