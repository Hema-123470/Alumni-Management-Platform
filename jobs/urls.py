from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list_view, name='job_list'),
    path('jobs/create/', views.job_create_view, name='job_create'),
    path('jobs/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('jobs/<int:job_id>/edit/', views.job_edit_view, name='job_edit'),
    path('jobs/<int:job_id>/delete/', views.job_delete_view, name='job_delete'),
    path('jobs/<int:job_id>/refer/', views.job_refer_view, name='job_refer'),
    path('jobs/<int:job_id>/referrals/', views.job_referrals_view, name='job_referrals'),
]
