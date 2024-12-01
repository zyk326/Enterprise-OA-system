from rest_framework.pagination import PageNumberPagination

class StaffListPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'size'
    page_size = 2