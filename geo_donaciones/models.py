from django.db import models
from donaredapp.models import Item as DonaredItem

# Create your models here.

class Item(DonaredItem):
    class Meta:
        proxy = True
        verbose_name = 'Item del Mapa'
        verbose_name_plural = 'Items del Mapa'
