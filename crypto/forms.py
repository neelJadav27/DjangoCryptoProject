from django import forms
from django.core.validators import RegexValidator
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class LogInForm(forms.Form):
    pwregex = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

    email = forms.CharField(label='Email', max_length=100,
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Email', 'class': 'input100', 'name': 'email'}))
    password = forms.CharField(label='Password', max_length=100,
                               validators=[
                                   RegexValidator(pwregex,
                                                  message="Should be a minimum eight characters, at least one letter, one number and one special character")],
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': '**********', 'class': 'input100', 'name': 'password'}))


class SignUpForm(forms.ModelForm):
    pwregex = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
                attrs={'id': 'password', 'name': 'password', 'class': 'input100', 'placeholder': '**********'}) ,validators=[
                                   RegexValidator(pwregex,
                                                  message="Should be a minimum eight characters, at least one letter, one number and one special character")],
 )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "sex", "dob", "phoneNo"]

        widgets = {
            'dob': DateInput(attrs={'class': 'label-input100', 'id': 'birthday', 'name': 'birthday'}),
            'first_name': forms.TextInput(
                attrs={'name': 'first_name', 'class': 'input100', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'name': 'last_name', 'class': 'input100', 'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'name': 'email', 'class': 'input100', 'placeholder': 'Email'}),
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
            'cardHolderName': forms.TextInput(
                attrs={'name': 'cardHolderName', 'id': 'cardHolderName', 'class': 'form-control mb-3',
                       'placeholder': 'John Doe'}),
            'cardNo': forms.TextInput(
                attrs={'name': 'cardNo', 'id': 'cardNo', 'class': 'form-control mb-3',
                       'placeholder': '1234123412341234'}),
            'expiryDate': forms.DateInput(
                attrs={'name': 'expiryDate', 'id': 'expiryDate', 'class': 'form-control mb-3', 'type': 'date',
                       'placeholder': ''}),
            'CVV': forms.PasswordInput(
                attrs={'name': 'CVV', 'id': 'CVV', 'class': 'form-control mb-3 pt-2',
                       'placeholder': '123'}),

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

    def __init__(self, *args, **kwargs):
        super(EditProfileDetails, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
