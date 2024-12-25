from django import forms
from .models import User,FeesHistory

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        label="Password",
        required=False  # Make password optional for editing users
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password",
        required=False  # Make confirm password optional for editing users
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password']  # Include fields you want to display

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Password matching validation only for new users (not when editing)
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # If a new password is provided, hash it and set it
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password
        
        if commit:
            user.save()
        return user

class FeesHistoryForm(forms.ModelForm):
    class Meta:
        model = FeesHistory
        fields = ['student', 'fee_type', 'amount_paid', 'payment_date']  # Add any other fields as needed
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }