from django.shortcuts import render
from django.http import JsonResponse
from donaredapp.models import Item
from django.core.serializers import serialize
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

# Vista para el mapa

@login_required
def mapa_items(request):
    # Obtener todos los items activos
    items = Item.objects.filter(activo=True)
    print(f"Total de items activos: {items.count()}")
    
    # Filtrar items con coordenadas
    items_con_coordenadas = items.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    print(f"Items con coordenadas: {items_con_coordenadas.count()}")
    
    # Imprimir detalles de cada item para depuración
    items_data = []
    for item in items_con_coordenadas:
        item_data = {
            'id': item.id,
            'nombre': item.nombre,
            'latitude': float(item.latitude) if item.latitude else None,
            'longitude': float(item.longitude) if item.longitude else None,
            'direccion': item.direccion
        }
        items_data.append(item_data)
        print(f"Item: {json.dumps(item_data, indent=2)}")
    
    context = {
        'items': items_con_coordenadas,
        'items_json': json.dumps(items_data),  # Para depuración en el template
        'debug': settings.DEBUG  # Agregar el modo debug al contexto
    }
    return render(request, 'geo_donaciones/mapa.html', context)

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
