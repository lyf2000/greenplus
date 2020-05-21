from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend
from blog.models import Post
from django.db.models import Func, F, Value

class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    # text = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Post
        fields = []


class PostTagFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.get('tags', None)
        if tags:
            tags = tags.split(',')
            queryset = queryset \
                .filter(tags__name__in=tags) \
                .annotate(num_tags=Count('tags')) \
                .filter(num_tags__gte=len(tags)).distinct()
        return queryset
