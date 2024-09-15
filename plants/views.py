from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Plant
from .serializers import PlantSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PlantCreateView(generics.CreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

class PlantDummyDataView(APIView):
    def get(self, request, format=None):
        dummy_data = {
            "species": "Leucojum vernum",
            "water": "Water once in 2 days, avoiding waterlogging to prevent root rot.",
            "light": "Partial shade to full shade conditions, tolerating some morning sun but avoiding direct sunlight in the afternoon.",
            "toxicity": "Toxic compounds that can be harmful to humans and animals if ingested, causing symptoms like nausea, vomiting, diarrhea, and abdominal pain.",
            "humidity": "Average humidity levels are suitable for this plant.",
            "common_names": ["Spring Snowflake"],
            "fertilizer": "Add compost or well-rotted manure to improve soil fertility and structure.",
            "health_status": "Healthy",
            "health_detail": "",
            "notes": "This plant is often associated with early spring and renewal due to its early blooming period. It is sometimes used in traditional spring festivals and celebrations. Its delicate white flowers are also a symbol of purity and innocence in some cultural contexts. Common uses include ornamental gardening and landscaping, often planted in woodland gardens, shaded borders, and rock gardens."
        }
        return Response(dummy_data, status=status.HTTP_200_OK)