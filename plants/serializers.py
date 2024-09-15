from rest_framework import serializers
from .models import Plant

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id', 'plant', 'species', 'details']
        extra_kwargs = {
            'details': {'read_only': True}
        }

        def create(self, validated_data):
            plant = Plant.objects.create(
                plant = validated_data['plant'],
                species = validated_data['species'],
            )
            return plant