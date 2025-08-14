import os
import django
from datetime import datetime, timezone
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chan_tickets.settings')
django.setup()

from tickets.models import Team, Venue, Match, TicketCategory, TicketPrice

def populate_teams():
    teams_data = [
        ('Kenya', 'KEN'),
        ('Morocco', 'MAR'),
        ('Angola', 'ANG'),
        ('DR Congo', 'DRC'),
        ('Zambia', 'ZAM'),
        ('Tanzania', 'TAN'),
        ('Madagascar', 'MAD'),
        ('Mauritania', 'MTN'),
        ('Burkina Faso', 'BFA'),
        ('Central African Republic', 'CTA'),
        ('Uganda', 'UGA'),
        ('Niger', 'NIG'),
        ('Guinea', 'GUI'),
        ('South Africa', 'RSA'),
        ('Algeria', 'ALG'),
        ('Senegal', 'SEN'),
        ('Congo', 'CGO'),
        ('Sudan', 'SDN'),
        ('Nigeria', 'NGA'),
    ]
    
    for name, code in teams_data:
        team, created = Team.objects.get_or_create(
            code=code,
            defaults={'name': name}
        )
        if created:
            print(f"Created team: {name}")

def populate_venues():
    venues_data = [
        ('Moi International Sports Centre Kasarani', 'Nairobi', 'Kenya', 60000),
        ('Nyayo National Stadium', 'Nairobi', 'Kenya', 30000),
        ('Benjamin Mkapa Stadium', 'Dar es Salaam', 'Tanzania', 60000),
        ('Amaan Stadium', 'Zanzibar', 'Tanzania', 15000),
        ('Mandela National Stadium', 'Kampala', 'Uganda', 45000),
    ]
    
    for name, city, country, capacity in venues_data:
        venue, created = Venue.objects.get_or_create(
            name=name,
            defaults={'city': city, 'country': country, 'capacity': capacity}
        )
        if created:
            print(f"Created venue: {name}")

def populate_ticket_categories():
    categories_data = [
        ('VIP', 'Premium seating with exclusive amenities'),
        ('Regular', 'Standard stadium seating'),
        ('Student', 'Discounted tickets for students with valid ID'),
    ]
    
    for name, description in categories_data:
        category, created = TicketCategory.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if created:
            print(f"Created ticket category: {name}")

def populate_matches():
    # Get teams and venues
    teams = {team.code: team for team in Team.objects.all()}
    venues = {venue.name: venue for venue in Venue.objects.all()}
    
    matches_data = [
        # Group A matches
        ('KEN', 'DRC', 'Moi International Sports Centre Kasarani', '2025-08-03 15:00', 'A'),
        ('ANG', 'ZAM', 'Nyayo National Stadium', '2025-08-03 18:00', 'A'),
        ('DRC', 'MAR', 'Nyayo National Stadium', '2025-08-07 17:00', 'A'),
        ('ANG', 'KEN', 'Moi International Sports Centre Kasarani', '2025-08-07 20:00', 'A'),
        ('KEN', 'MAR', 'Moi International Sports Centre Kasarani', '2025-08-10 15:00', 'A'),
        ('ZAM', 'ANG', 'Nyayo National Stadium', '2025-08-10 18:00', 'A'),
        ('MAR', 'ZAM', 'Nyayo National Stadium', '2025-08-14 17:00', 'A'),
        ('ANG', 'DRC', 'Moi International Sports Centre Kasarani', '2025-08-14 20:00', 'A'),
        ('DRC', 'MAR', 'Nyayo National Stadium', '2025-08-17 15:00', 'A'),
        ('ZAM', 'KEN', 'Moi International Sports Centre Kasarani', '2025-08-17 15:00', 'A'),
        
        # Group B matches
        ('TAN', 'MAD', 'Benjamin Mkapa Stadium', '2025-08-02 19:00', 'B'),
        ('BFA', 'MTN', 'Benjamin Mkapa Stadium', '2025-08-02 20:00', 'B'),
        ('TAN', 'BFA', 'Benjamin Mkapa Stadium', '2025-08-06 17:00', 'B'),
        ('MAD', 'MTN', 'Benjamin Mkapa Stadium', '2025-08-06 20:00', 'B'),
        ('MTN', 'CTA', 'Benjamin Mkapa Stadium', '2025-08-11 17:00', 'B'),
        ('MAD', 'BFA', 'Benjamin Mkapa Stadium', '2025-08-11 20:00', 'B'),
        ('CTA', 'TAN', 'Benjamin Mkapa Stadium', '2025-08-15 17:00', 'B'),
        ('MTN', 'MAD', 'Benjamin Mkapa Stadium', '2025-08-15 20:00', 'B'),
        
        # Group C matches
        ('UGA', 'ALG', 'Mandela National Stadium', '2025-08-04 17:00', 'C'),
        ('NIG', 'GUI', 'Mandela National Stadium', '2025-08-04 20:00', 'C'),
        ('GUI', 'RSA', 'Mandela National Stadium', '2025-08-08 17:00', 'C'),
        ('UGA', 'NIG', 'Mandela National Stadium', '2025-08-08 20:00', 'C'),
        ('NIG', 'RSA', 'Mandela National Stadium', '2025-08-12 17:00', 'C'),
        ('GUI', 'ALG', 'Mandela National Stadium', '2025-08-12 20:00', 'C'),
        ('RSA', 'UGA', 'Mandela National Stadium', '2025-08-16 17:00', 'C'),
        ('ALG', 'NIG', 'Mandela National Stadium', '2025-08-16 20:00', 'C'),
        
        # Group D matches
        ('SEN', 'CGO', 'Nyayo National Stadium', '2025-08-05 17:00', 'D'),
        ('SDN', 'NGA', 'Nyayo National Stadium', '2025-08-05 20:00', 'D'),
        ('CGO', 'SDN', 'Nyayo National Stadium', '2025-08-09 17:00', 'D'),
        ('SEN', 'NGA', 'Nyayo National Stadium', '2025-08-09 20:00', 'D'),
        ('SDN', 'NGA', 'Nyayo National Stadium', '2025-08-13 17:00', 'D'),
        ('CGO', 'SEN', 'Nyayo National Stadium', '2025-08-13 20:00', 'D'),
        ('ALG', 'NIG', 'Nyayo National Stadium', '2025-08-18 20:00', 'D'),
    ]
    
    for home_code, away_code, venue_name, date_str, group in matches_data:
        if home_code in teams and away_code in teams and venue_name in venues:
            match_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
            
            match, created = Match.objects.get_or_create(
                home_team=teams[home_code],
                away_team=teams[away_code],
                venue=venues[venue_name],
                date_time=match_datetime,
                defaults={'group': group}
            )
            if created:
                print(f"Created match: {home_code} vs {away_code}")

def populate_ticket_prices():
    categories = {cat.name: cat for cat in TicketCategory.objects.all()}
    matches = Match.objects.all()
    
    # Base prices in different currencies
    base_prices = {
        'VIP': {'KES': 1000, 'UGX': 15000, 'TZS': 25000},
        'Regular': {'KES': 500, 'UGX': 7500, 'TZS': 12500},
        'Student': {'KES': 200, 'UGX': 3000, 'TZS': 5000},
    }
    
    for match in matches:
        for cat_name, category in categories.items():
            ticket_price, created = TicketPrice.objects.get_or_create(
                match=match,
                category=category,
                defaults={
                    'price_kes': Decimal(str(base_prices[cat_name]['KES'])),
                    'price_ugx': Decimal(str(base_prices[cat_name]['UGX'])),
                    'price_tzs': Decimal(str(base_prices[cat_name]['TZS'])),
                    'available_quantity': 1000 if cat_name == 'Regular' else 200,
                }
            )
            if created:
                print(f"Created ticket price for {match} - {cat_name}")

if __name__ == '__main__':
    print("Populating database with CHAN tournament data...")
    populate_teams()
    populate_venues()
    populate_ticket_categories()
    populate_matches()
    populate_ticket_prices()
    print("Database population completed!")

