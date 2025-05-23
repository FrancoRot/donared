from django.urls import path
from . import views

app_name = 'geo_donaciones'

urlpatterns = [
    path('mapa/', views.mapa_items, name='mapa'),
    path('mapa/api/items/', views.items_geojson, name='items_geojson'),
] 