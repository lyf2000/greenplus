import django_filters

from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget


from blog.models import Post


# class PostFilter(django_filters.FilterSet):
#
#     title = django_filters.CharFilter(lookup_expr='icontains')
#     # tags = TagField(required=False, widget=LabelWidget)
#
#     class Meta:
#         model = Post
#         fields = ['author']