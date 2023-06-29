from rest_framework_gis import serializers
from .models import Building


class BuildingSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        model = Building
        geo_field = 'geom'
        fields = '__all__'
