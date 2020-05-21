from rest_framework.pagination import PageNumberPagination, CursorPagination


class MyPaginator(PageNumberPagination):
    page_size = 5
    max_page_size = 20
