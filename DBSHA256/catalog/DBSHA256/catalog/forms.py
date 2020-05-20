from django import forms
from .models import Release

class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        fields = ("name", "ip", "port", "database", "user", "password", )   # NOTE: the trailing comma is required