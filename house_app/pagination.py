from rest_framework.pagination import PageNumberPagination
class PropertyPageNumberPagination(PageNumberPagination):
    page_size = 3

class ReviewPageNumberPagination(PageNumberPagination):
    page_size = 4