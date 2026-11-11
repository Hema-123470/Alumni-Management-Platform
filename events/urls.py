from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list_view, name='event_list'),
    path('events/create/', views.event_create_view, name='event_create'),
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('events/<int:event_id>/edit/', views.event_edit_view, name='event_edit'),
    path('events/<int:event_id>/delete/', views.event_delete_view, name='event_delete'),
    path('events/<int:event_id>/register/', views.event_register_view, name='event_register'),
]
