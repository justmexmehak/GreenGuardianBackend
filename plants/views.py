from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Plant
from .serializers import PlantSerializer

class PlantCreateView(generics.CreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer