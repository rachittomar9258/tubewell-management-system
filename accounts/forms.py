from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignUpForm(UserCreationForm):

    role = forms.ChoiceField(
        choices=(('owner', 'Owner'), ('renter', 'Renter')),
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Phone Number'
        })
    )

    village = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Village Name'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'phone_number',
            'village',
            'role',
            'password1',
            'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create Password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })


class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'village', 'fast2sms_api_key']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter Phone Number'
            }),
            'village': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter Village Name'
            }),
            'fast2sms_api_key': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Fast2SMS API Key'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user and user.role != 'owner':
            self.fields.pop('fast2sms_api_key')