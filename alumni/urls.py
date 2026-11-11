from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.my_profile_view, name='my_profile'),
    path('profile/<int:user_id>/', views.view_profile_view, name='view_profile'),
    path('alumni-list/', views.alumni_list_view, name='alumni_list'),
]
