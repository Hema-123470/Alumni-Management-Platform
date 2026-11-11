from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.reports_dashboard_view, name='reports_dashboard'),
    path('reports/alumni/', views.alumni_report_view, name='alumni_report'),
    path('reports/alumni/export/', views.export_alumni_csv, name='export_alumni_csv'),
    path('reports/donations/', views.donation_report_view, name='donation_report'),
    path('reports/events/', views.event_report_view, name='event_report'),
    path('reports/jobs/', views.job_report_view, name='job_report'),
]
