from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Plant
from .serializers import PlantSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import requests
import json
import os
import re

from together import Together

class PlantCreateView(generics.CreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def perform_create(self, serializer):
        plant = serializer.save()
        # Assuming the image ID is part of the plant model
        image_id = plant.id
        self.request.session['image_id'] = image_id
        print("Saved image id ", self.request.session["image_id"])


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

class PlantDetailView(APIView):
    def get(self, request, *args, **kwargs):
        image_id = request.query_params.get('image_id')
        # image_id = request.session.get('image_id')
        print(f'Got image id {image_id}')
        if not image_id:
            return Response({"error": "Image ID not found"}, status=status.HTTP_400_BAD_REQUEST)
        plant = Plant.objects.get(id=image_id)
        data = get_plant_details(plant.plant.path)
        plant.details = data
        plant.save()
        return Response(data, status=status.HTTP_200_OK)


def encode_image(img_path):
    with open(img_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def get_access_token(encoded_image):
    base_url = os.getenv('BASE_URL_ID')
    payload = json.dumps({
        "images": [
            f'{encoded_image}'
        ],
        'health': 'auto'
    })
    headers = {
        'Api-Key': os.getenv('PLANT_ID_API_KEY'),
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", base_url, headers=headers, data=payload)
    dictionary = json.loads(response.text)
    return dictionary['access_token']

def get_plant_details(img_path):
    encoded_image = encode_image(img_path)
    access_token = get_access_token(encoded_image)
    url = f"{os.getenv('BASE_URL_ID')}/{access_token}"
    print(url)
    payload={}
    headers = {
    'Api-Key': 'eEiif34haxNNMZGmSED2RyllwhSTbcpns9ZnHZkSt2SwuLx7tY',
    'Content-Type': 'application/json'
    }
    params = {
        'details': 'common_names,description,watering,propagation_methods,best_watering,best_light_condition,best_soil_type,common_uses,toxicity,cultural_significance, cause, treatment'
    }
    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    print(response.text)
    return get_plan_json(response.text)

def get_plan_json(res):
    client = Together(api_key = os.getenv('TOGETHER_API_KEY'))

    response = client.chat.completions.create(
        model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
                {
                    "role": "system",
                    "content": 
                        '''
                            You are a plant care specialist. Based on the species and other details provided, you will output a structured JSON with the following fields: species, water, light, toxicity, humidity, common names, fertilizer, health status, health detail (leave empty if health status is healthy), and notes. Ensure the output is in valid JSON format.

                            Keep your tone friendly and accessible, but avoid overly simplistic language. Assume the user has basic knowledge about plants.

                            Guidelines:
                            1. If there is no information about the plant's health, assume the plant is healthy.
                            2. Include additional details in the notes, such as cultural significance or common uses.
                            3. If any information is unspecified or missing, provide an appropriate average value instead of leaving it null.
                            4. For the water field, interpret the min and max values as the plant's preferred moisture level (1 = dry, 2 = medium, 3 = wet). For example, "watering": {"min": 1, "max": 2} should be translated to a sentence like "This plant prefers a dry to medium moisture environment." Additionally, specify how often the plant should be watered, such as "Water once every 2 days."
                            5. In the health detail, only use the first disease listed in the JSON, as it has the highest probability. Include information on how to treat it.

                            Example output:
                            {
                            "species": "Glycine max",
                            "water": "Consistent moisture, especially during its growing season. Overwatering can lead to root rot, while underwatering can stress the plant and reduce yield. Water once every 2 days.",
                            "light": "This plant thrives in full sunlight. It needs at least six to eight hours of direct sunlight each day to grow well. Insufficient light can lead to weak, spindly growth and lower yields.",
                            "toxicity": "This plant is generally non-toxic to humans and animals. It is widely consumed as food and used in various products without adverse effects.",
                            "humidity": "Average humidity levels are suitable for this plant.",
                            "common_names": ["soybean"],
                            "fertilizer": "A balanced fertilizer applied once a month during the growing season is beneficial.",
                            "health_status": "Unhealthy",
                            "health_detail": "Insecta (Class Insecta contains many major plant pests such as aphids and thrips. Damage can be caused by both larval and adult stages. They can cause feeding damage or transmit a bacterial, viral, or fungal infection. Treatment: Use insecticidal soap or neem oil to control the pests.)",
                            "notes": "This plant is incredibly versatile and has a wide range of uses. It is a major source of protein and is used to make products like tofu, soy milk, and tempeh. It is also processed into oil, which is used in cooking and as an ingredient in many processed foods. Additionally, it is used in animal feed, industrial products, and even as a biofuel. Its by-products, such as meal and hulls, are valuable in various industries, making it an economically important crop."
                            }
                        '''
                },
                {
                    "role": "user",
                    "content": res
                }
        ],
        max_tokens=1024,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>", "<|eom_id|>"],
        stream=False
    )

    print(response)
    print(response.choices[0].message.content)

    response_content = response.choices[0].message.content

    # Use regular expressions to extract JSON part of the response
    json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        response_json = json.loads(json_str)
        return response_json
    else:
        raise ValueError("No JSON content found in the response")
    

