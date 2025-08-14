from django.contrib import admin
from .models import Team, Venue, Match, TicketCategory, TicketPrice, Booking, Ticket

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'capacity']
    list_filter = ['country', 'city']
    search_fields = ['name', 'city']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['home_team', 'away_team', 'venue', 'date_time', 'group', 'match_type', 'is_completed']
    list_filter = ['group', 'match_type', 'is_completed', 'venue']
    search_fields = ['home_team__name', 'away_team__name']
    date_hierarchy = 'date_time'

@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

class TicketPriceInline(admin.TabularInline):
    model = TicketPrice
    extra = 1

@admin.register(TicketPrice)
class TicketPriceAdmin(admin.ModelAdmin):
    list_display = ['match', 'category', 'price_kes', 'price_ugx', 'price_tzs', 'available_quantity']
    list_filter = ['category', 'match__group']
    search_fields = ['match__home_team__name', 'match__away_team__name', 'category__name']

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = ['ticket_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'customer_name', 'ticket_price', 'quantity', 'total_amount', 'currency', 'payment_status', 'created_at']
    list_filter = ['payment_status', 'currency', 'payment_method', 'created_at']
    search_fields = ['booking_reference', 'customer_name', 'customer_email']
    readonly_fields = ['booking_reference', 'total_amount', 'created_at', 'updated_at']
    inlines = [TicketInline]

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'booking', 'is_used']
    list_filter = ['is_used']
    search_fields = ['ticket_number', 'booking__booking_reference']
    readonly_fields = ['ticket_number']
