from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        body_list = [
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_count', self.page.paginator.num_pages),
        ]
        if 'question_count' in data:
            body_list.append(('question_count', data['question_count']))
            body_list.append(('results', data['results']))
        else:
            body_list.append(('results', data))

        return Response(OrderedDict(body_list))


class PageNumberPagination_10(CustomPagination):

    page_size = 10


class PageNumberPagination_20(CustomPagination):
    page_size = 20

class PageNumberPagination_100(CustomPagination):
    page_size = 100


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


