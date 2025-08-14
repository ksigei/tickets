from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Match, Team, Venue, TicketPrice, TicketCategory, Booking, Ticket
from .forms import BookingForm
import json
from decimal import Decimal

def home(request):
    """Home page showing upcoming matches"""
    upcoming_matches = Match.objects.filter(
        date_time__gte=timezone.now(),
        is_completed=False
    ).order_by('date_time')[:6]
    
    context = {
        'upcoming_matches': upcoming_matches,
    }
    return render(request, 'tickets/home.html', context)

def matches(request):
    """List all matches with filtering options"""
    matches_list = Match.objects.filter(
        date_time__gte=timezone.now(),
        is_completed=False
    ).order_by('date_time')
    
    # Filter by group
    group_filter = request.GET.get('group')
    if group_filter:
        matches_list = matches_list.filter(group=group_filter)
    
    # Filter by team
    team_filter = request.GET.get('team')
    if team_filter:
        matches_list = matches_list.filter(
            Q(home_team__code=team_filter) | Q(away_team__code=team_filter)
        )
    
    # Filter by venue
    venue_filter = request.GET.get('venue')
    if venue_filter:
        matches_list = matches_list.filter(venue__id=venue_filter)
    
    # Pagination
    paginator = Paginator(matches_list, 10)
    page_number = request.GET.get('page')
    matches_page = paginator.get_page(page_number)
    
    # Get filter options
    teams = Team.objects.all().order_by('name')
    venues = Venue.objects.all().order_by('name')
    groups = [('A', 'Group A'), ('B', 'Group B'), ('C', 'Group C'), ('D', 'Group D')]
    
    context = {
        'matches': matches_page,
        'teams': teams,
        'venues': venues,
        'groups': groups,
        'current_group': group_filter,
        'current_team': team_filter,
        'current_venue': venue_filter,
    }
    return render(request, 'tickets/matches.html', context)

def match_detail(request, match_id):
    """Match detail page with ticket booking options"""
    match = get_object_or_404(Match, id=match_id)
    ticket_prices = TicketPrice.objects.filter(match=match).select_related('category')
    
    context = {
        'match': match,
        'ticket_prices': ticket_prices,
    }
    return render(request, 'tickets/match_detail.html', context)

def book_ticket(request, match_id):
    """Ticket booking page"""
    match = get_object_or_404(Match, id=match_id)
    ticket_prices = TicketPrice.objects.filter(match=match).select_related('category')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            # Calculate total amount based on selected currency
            ticket_price = booking.ticket_price
            if booking.currency == 'UGX':
                unit_price = ticket_price.price_ugx
            elif booking.currency == 'KES':
                unit_price = ticket_price.price_kes
            else:  # TZS
                unit_price = ticket_price.price_tzs
            
            booking.total_amount = unit_price * booking.quantity
            booking.save()
            
            # Create individual tickets
            for i in range(booking.quantity):
                Ticket.objects.create(booking=booking)
            
            messages.success(request, f'Booking created successfully! Reference: {booking.booking_reference}')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'match': match,
        'ticket_prices': ticket_prices,
        'form': form,
    }
    return render(request, 'tickets/book_ticket.html', context)

def booking_confirmation(request, booking_id):
    """Booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id)
    tickets = Ticket.objects.filter(booking=booking)
    
    context = {
        'booking': booking,
        'tickets': tickets,
    }
    return render(request, 'tickets/booking_confirmation.html', context)

@csrf_exempt
def get_ticket_prices(request):
    """AJAX endpoint to get ticket prices for a match"""
    if request.method == 'POST':
        data = json.loads(request.body)
        match_id = data.get('match_id')
        currency = data.get('currency', 'KES')
        
        try:
            match = Match.objects.get(id=match_id)
            ticket_prices = TicketPrice.objects.filter(match=match).select_related('category')
            
            prices_data = []
            for tp in ticket_prices:
                if currency == 'UGX':
                    price = float(tp.price_ugx)
                elif currency == 'KES':
                    price = float(tp.price_kes)
                else:  # TZS
                    price = float(tp.price_tzs)
                
                prices_data.append({
                    'id': tp.id,
                    'category': tp.category.name,
                    'description': tp.category.description,
                    'price': price,
                    'available_quantity': tp.available_quantity,
                    'currency': currency
                })
            
            return JsonResponse({'success': True, 'prices': prices_data})
        except Match.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Match not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def search_matches(request):
    """Search matches by team names or venue"""
    query = request.GET.get('q', '')
    matches_list = Match.objects.filter(
        date_time__gte=timezone.now(),
        is_completed=False
    )
    
    if query:
        matches_list = matches_list.filter(
            Q(home_team__name__icontains=query) |
            Q(away_team__name__icontains=query) |
            Q(venue__name__icontains=query) |
            Q(venue__city__icontains=query)
        )
    
    matches_list = matches_list.order_by('date_time')
    
    # Pagination
    paginator = Paginator(matches_list, 10)
    page_number = request.GET.get('page')
    matches_page = paginator.get_page(page_number)
    
    context = {
        'matches': matches_page,
        'query': query,
    }
    return render(request, 'tickets/search_results.html', context)
