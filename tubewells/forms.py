from django import forms
from .models import Tubewell


class TubewellForm(forms.ModelForm):
    class Meta:
        model = Tubewell
        fields = ['name', 'location', 'rate_per_hour']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tubewell ka naam'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Location'
            }),
            'rate_per_hour': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rate per hour'
            }),
        }


class AddRenterForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label="Renter ka naam",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Renter ka naam'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        label="Renter ka phone number",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Renter ka phone number'
        })
    )

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number'].strip()
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Sahi 10-digit phone number daalo.")
        return phone


class EditRenterForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label="Renter ka naam",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Renter ka naam'
        })
    )