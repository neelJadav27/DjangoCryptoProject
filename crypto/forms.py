from django import forms

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class LogInForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100,
                            widget=forms.EmailInput(attrs={'placeholder': 'Username', 'class': 'input-field'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-field'}))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name","email", "password", "sex", "dob", "phoneNo"]
        widgets = {
            'dob': DateInput(),
            'password': forms.PasswordInput(),
        }


class Crypto(forms.ModelForm):
    class Meta:
        model = Crypto
        fields = ['name', 'alias']
