from typing import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('current', self.page.number),
            ('results', data)
        ]))
