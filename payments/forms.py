from django import forms


class OwnerPaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=1, label="Amount Received")