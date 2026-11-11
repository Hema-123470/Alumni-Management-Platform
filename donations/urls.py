from django.urls import path
from . import views

urlpatterns = [
    path('donations/', views.donation_list_view, name='donation_list'),
    path('donations/make/', views.make_donation_view, name='make_donation'),
    path('sponsorships/', views.sponsorship_list_view, name='sponsorship_list'),
    path('sponsorships/create/', views.sponsorship_create_view, name='sponsorship_create'),
    path('sponsorships/<int:sponsorship_id>/edit/', views.sponsorship_edit_view, name='sponsorship_edit'),
    path('sponsorships/<int:sponsorship_id>/delete/', views.sponsorship_delete_view, name='sponsorship_delete'),
]
