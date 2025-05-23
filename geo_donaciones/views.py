from django.shortcuts import render
from django.http import JsonResponse
from donaredapp.models import Item
from django.core.serializers import serialize
from django.conf import settings

# Create your views here.

# Vista para el mapa

def mapa(request):
    return render(request, 'geo_donaciones/mapa.html')

# API GeoJSON para items con coordenadas

def items_geojson(request):
    items = Item.objects.filter(activo=True, latitude__isnull=False, longitude__isnull=False)
    features = []
    
    for item in items:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(item.longitude), float(item.latitude)]
            },
            'properties': {
                'id': item.id,
                'nombre': item.nombre,
                'descripcion': item.descripcion,
                'imagen': item.imagen.url if item.imagen else None
            }
        }
        features.append(feature)
    
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return JsonResponse(geojson)
