from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),  # Map root URL to ticket_list view
]
