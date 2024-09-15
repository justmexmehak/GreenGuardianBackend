from django.urls import path
from .views import *

urlpatterns = [
    path('create/', PlantCreateView.as_view(), name='plant-create'),
    path('detail/', PlantDummyDataView.as_view(), name='plant-dummy-data'),
    path('detail2/', PlantDetailView.as_view(), name='plant-detail'),
]