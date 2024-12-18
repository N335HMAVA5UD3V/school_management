from django import forms
from .models import User
from django.contrib import messages



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "email", "role", "address", "district", "state", "pin_code", "is_active","password","username"]
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "username": "Username",
            "password": 'Password',
            "role": "User Role",
            "address": "Residential Address",
            "district": "District",
            "state": "State",
            "pin_code": "Postal Code",
            "is_active": "Active Status",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Enter a valid email address", "class": "form-control"}),
            "pin_code": forms.TextInput(attrs={"placeholder": "Enter 6-digit PIN", "class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),  # Dropdown for ROLE_CHOICES
        }

    def clean_pin_code(self):
        pin_code = self.cleaned_data.get("pin_code")
        if len(pin_code) != 6:
            raise forms.ValidationError("PIN code must be 6 digits long.")
        return pin_code

