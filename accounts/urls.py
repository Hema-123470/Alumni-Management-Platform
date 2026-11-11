from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('pending-approvals/', views.pending_approvals_view, name='pending_approvals'),
    path('approve/<int:user_id>/', views.approve_user_view, name='approve_user'),
    path('reject/<int:user_id>/', views.reject_user_view, name='reject_user'),
]
