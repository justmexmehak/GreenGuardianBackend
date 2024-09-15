from django.urls import path
from .views import PlantCreateView

urlpatterns = [
    path('create/', PlantCreateView.as_view(), name='plant-create'),
    path('detail/', PlantDummyDataView.as_view(), name='plant-dummy-data'),
]