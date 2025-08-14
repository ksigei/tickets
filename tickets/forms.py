from django import forms
from .models import Booking, TicketPrice

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'ticket_price', 'quantity', 'currency', 'payment_method',
            'customer_name', 'customer_email', 'customer_phone'
        ]
        widgets = {
            'ticket_price': forms.Select(attrs={'class': 'form-control', 'id': 'ticket_price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'currency': forms.Select(attrs={'class': 'form-control', 'id': 'currency'}),
            'payment_method': forms.Select(attrs={'class': 'form-control', 'id': 'payment_method'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }
    
    def __init__(self, *args, **kwargs):
        match = kwargs.pop('match', None)
        super().__init__(*args, **kwargs)
        
        if match:
            self.fields['ticket_price'].queryset = TicketPrice.objects.filter(match=match)
        
        # Update payment method choices based on currency
        self.fields['payment_method'].choices = [
            ('', 'Select Payment Method'),
            ('mpesa_ke', 'M-Pesa (Kenya)'),
            ('airtel_ke', 'Airtel Money (Kenya)'),
            ('mtn_ug', 'MTN Mobile Money (Uganda)'),
            ('airtel_ug', 'Airtel Money (Uganda)'),
            ('mpesa_tz', 'M-Pesa (Tanzania)'),
            ('tigo_tz', 'Tigo Pesa (Tanzania)'),
            ('visa', 'Visa Card'),
            ('mastercard', 'Mastercard'),
            ('amex', 'American Express'),
        ]
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        ticket_price = self.cleaned_data.get('ticket_price')
        
        if ticket_price and quantity:
            if quantity > ticket_price.available_quantity:
                raise forms.ValidationError(f'Only {ticket_price.available_quantity} tickets available for this category.')
        
        return quantity

