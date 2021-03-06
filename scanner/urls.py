from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("graph", views.graph_data, name="graph"),
    path("suspects", views.suspects, name="suspects"),
    path("account/<pk>", views.StellarAccountDetailView.as_view(), name="account"),
]
