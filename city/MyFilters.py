from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import ParseError

class AreaFilter(BaseFilterBackend):
    '''get format: ?area=min_area,max_area'''
    area_param = 'area'  # The URL query parameter which contains the

    def get_filter_area(self, request, **kwargs):
        area_string = request.query_params.get(self.area_param, None)

        if not area_string:
            return None
        try:
            (min_area, max_area) = (float(n) for n in area_string.split(','))
        except ValueError:
            raise ParseError(
                'Invalid geometry string supplied for parameter {0}'.format(
                    self.area_param
                )
            )

        return (min_area, max_area)

    def filter_queryset(self, request, queryset, view):
        filter_field = getattr(view, 'area_filter_field', None)

        if not filter_field:
            return queryset

        areas = self.get_filter_area(request)
        if not areas:
            return queryset

        min_area, max_area = self.get_filter_area(request)
        allowed_pks = []
        try:
            for obj in queryset:
                area = obj.geom.area
                if area >= min_area and area <= max_area:
                    allowed_pks.append(obj.pk)
        except Exception as e:
            raise Exception(e)

        return queryset.filter(
            pk__in = allowed_pks
        )

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": self.area_param,
                "required": False,
                "in": "query",
                "description": "max and min area for filter "
                "Represents **point** in **Distance to point filter**",
                "schema": {
                    "type": "array",
                    "items": {"type": "float"},
                    "minItems": 2,
                    "maxItems": 2,
                    "example": [0, 10],
                },
                "style": "form",
                "explode": False,
            },
        ]
