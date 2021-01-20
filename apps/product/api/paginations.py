from rest_framework.pagination import LimitOffsetPagination


class CustomOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 50

    # def get_paginated_response(self, data):
