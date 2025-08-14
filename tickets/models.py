from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Team(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)
    flag_image = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Venue(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    capacity = models.IntegerField()
    
    def __str__(self):
        return f"{self.name}, {self.city}"

class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    group = models.CharField(max_length=1, choices=[('A', 'Group A'), ('B', 'Group B'), ('C', 'Group C'), ('D', 'Group D')])
    match_type = models.CharField(max_length=20, choices=[
        ('group', 'Group Stage'),
        ('quarter', 'Quarter Final'),
        ('semi', 'Semi Final'),
        ('third', '3rd Place'),
        ('final', 'Final')
    ], default='group')
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.home_team.code} vs {self.away_team.code} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"

class TicketCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class TicketPrice(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='ticket_prices')
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    price_ugx = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    price_kes = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    price_tzs = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    available_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ['match', 'category']
    
    def __str__(self):
        return f"{self.match} - {self.category.name}"

class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ticket_price = models.ForeignKey(TicketPrice, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('UGX', 'Uganda Shillings'), ('KES', 'Kenya Shillings'), ('TZS', 'Tanzania Shillings')])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    booking_reference = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking {self.booking_reference} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import random
            import string
            self.booking_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=20, unique=True)
    qr_code = models.TextField(blank=True, null=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Ticket {self.ticket_number}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            import random
            import string
            self.ticket_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        super().save(*args, **kwargs)
