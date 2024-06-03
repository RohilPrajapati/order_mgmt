from django.urls import path
from .views import CompanyListView,CompanyDetailView

urlpatterns = [
    path('', CompanyListView.as_view(), name="company_list"),
    path('<int:pk>/', CompanyDetailView.as_view(), name="company_detail"),
]