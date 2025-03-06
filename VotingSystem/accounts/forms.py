from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, VerificationCode

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    registration_number = forms.CharField(max_length=20, required=True)
    faculty = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'registration_number',
            'faculty',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_registration_number(self):
        reg_number = self.cleaned_data.get('registration_number')
        if User.objects.filter(registration_number=reg_number).exists():
            raise ValidationError("This registration number is already registered.")
        return reg_number

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your registered email',
            'class': 'form-control'
        })
    )
    registration_number = forms.CharField(
        label='Registration Number',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your registration number',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        registration_number = cleaned_data.get('registration_number')

        # Additional validation if needed
        if email and registration_number:
            user = User.objects.filter(email=email, registration_number=registration_number).first()
            if not user:
                raise forms.ValidationError("Invalid email or registration number.")

        return cleaned_data

class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        label='Verification Code',
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 6-digit code',
            'class': 'form-control'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("Verification code must be a 6-digit number.")
        return code