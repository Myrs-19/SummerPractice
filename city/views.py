from django.shortcuts import render
from rest_framework import viewsets
from rest_framework_gis.filters import DistanceToPointFilter


from .models import Building
from .serializers import BuildingSerializer
from .MyFilters import AreaFilter


# https://github.com/openwisp/django-rest-framework-gis#distancetopointfilter
class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    distance_filter_field = "geom"
    area_filter_field = "geom"
    filter_backends = (DistanceToPointFilter, AreaFilter)