from django import forms

from .models import Crypto

class LogInForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'input-field'}))
    password = forms.CharField(label='Password', max_length=100 , widget=forms.TextInput(attrs={'placeholder': 'Password','class': 'input-field'}))


class SignUpForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
    phoneNo = forms.CharField(label='Phone No', max_length=100)

class Crypto(forms.ModelForm):
    class Meta:
        model = Crypto
        fields = ['name','alias']