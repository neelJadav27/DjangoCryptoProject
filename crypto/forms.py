from django import forms

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class LogInForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Email', 'class': 'input100', 'name': 'email'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': '**********', 'class': 'input100', 'name': 'password'}))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "sex", "dob", "phoneNo"]
        widgets = {
            'dob': DateInput(attrs={'class': 'label-input100', 'id': 'birthday', 'name': 'birthday'}),
            'first_name': forms.TextInput(
                attrs={'name': 'first_name', 'class': 'input100', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'name': 'last_name', 'class': 'input100', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'name': 'email', 'class': 'input100', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(
                attrs={'name': 'password', 'class': 'input100', 'placeholder': '**********'}),
            'sex': forms.Select(attrs={'name': 'sex', 'class': 'label-input100', 'placeholder': 'Sex'}),
            'phoneNo': forms.TextInput(
                attrs={'name': 'phoneNo', 'class': 'input100', 'placeholder': 'Phone Number',
                       'maxlength': 10, 'minlength': 10})}


class Crypto(forms.ModelForm):
    class Meta:
        model = Crypto
        fields = ['name', 'alias']


class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['cardHolderName', 'cardNo', 'expiryDate', 'CVV']
        widgets = {
            'expiryDate': forms.DateInput(attrs={'id': 'expiryDate', 'name': 'expiryDate', 'type': 'date'})
        }


class MakePaymentForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['userId', 'crypto', 'cryptoRate', 'amount', 'type', 'paymentDate', 'quantity']

        '''userId = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    cryptoRate = models.FloatField(null=False, blank=False)
    buyRate = models.FloatField(null=False, blank=False)
    quantity = models.FloatField(null=False, blank=False)
    operationChoice = [('B', "Buy"), ('S', "Sell")]
    type = models.CharField(max_length=1, choices=operationChoice, default='B')
    paymentDate = models.DateField(default=datetime.now())
'''


class EditProfileDetails(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phoneNo"]
