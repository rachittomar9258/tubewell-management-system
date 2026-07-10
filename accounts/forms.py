from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=(('owner', 'Owner'), ('renter', 'Renter')))
    phone_number = forms.CharField(max_length=15, required=True)
    village = forms.CharField(max_length=100, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'phone_number', 'village', 'role', 'password1', 'password2')