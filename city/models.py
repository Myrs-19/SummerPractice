from django.db import models
from django.contrib.gis.db import models as models_geo


# Create your models here.
class Building(models_geo.Model):
    geom = models_geo.PolygonField(srid=4326)
    address = models.CharField(max_length=255, blank=False)
