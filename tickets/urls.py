from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('matches/', views.matches, name='matches'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('book/<int:match_id>/', views.book_ticket, name='book_ticket'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('api/ticket-prices/', views.get_ticket_prices, name='get_ticket_prices'),
    path('search/', views.search_matches, name='search_matches'),
]

