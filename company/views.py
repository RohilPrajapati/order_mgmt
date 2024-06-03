from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAdminUser


# Create your views here.

class CompanyListView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
