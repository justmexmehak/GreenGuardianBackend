from django.urls import path
from .views import PlantCreateView

urlpatterns = [
    path('create/', PlantCreateView.as_view(), name='plant-create'),
]