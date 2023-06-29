from rest_framework.test import APITestCase
from .models import Building
from django.contrib.gis.geos import Polygon, Point

class BuildingTests(APITestCase):
    path = r'http://127.0.0.1:8000/api/city/buildings/'

    @classmethod
    def setUpTestData(cls):
        pol = Polygon(((0.0, 0.0), (0.0, 5.0), (5.0, 5.0), (5.0, 0.0), (0.0, 0.0)))
        Building.objects.create(geom=pol, address="test1")

        pol = Polygon(((100.0, 100.0), (100.0, 150.0), (200.0, 150.0), (200.0, 100.0), (100.0, 100.0)))
        Building.objects.create(geom=pol, address="test2")

    def test_filter_area(self):
        min_area = 0.0
        max_area = 25.0

        url = self.path
        data = {'area' : f"{min_area},{max_area}"}
        response = self.client.get(url, data)
        amount_features_received = len(response.data['features'])

        buildings = Building.objects.all()
        amount_real_features = 0
        for building in buildings:
            area = building.geom.area
            if min_area <= area <=max_area:
                amount_real_features += 1

        self.assertEqual(amount_features_received, amount_real_features, "Nice or not nice")


    def test_filter_distance_to_point(self):
        dist = 100
        x = 0.0
        y = 0.0
        point = Point(x, y)

        url = self.path
        data = {'dist' : dist, 'point' : f"{point.x},{point.y}"}
        response = self.client.get(url, data)
        amount_features_received = len(response.data['features'])

        buildings = Building.objects.all()
        amount_real_features = 0
        for building in buildings:
            distance = building.geom.distance(point)
            if distance <= dist:
                amount_real_features += 1

        self.assertEqual(amount_features_received, amount_real_features, "Nice or not nice")