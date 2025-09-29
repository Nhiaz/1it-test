from django.urls import path
from . import views

urlpatterns = [
    path("", views.cashflow_list, name="cashflow_list"),
    path("new/", views.cashflow_create, name="cashflow_create"),
    path("<int:pk>/edit/", views.cashflow_update, name="cashflow_update"),
]
