from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from taggit.models import Tag

from blog.api.filters import PostTagFilter
from blog.api.paginators import MyPaginator
from blog.api.serializers import PostSerializer, TagSerializer
from blog.models import Post


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """

    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = MyPaginator
    filter_backends = (SearchFilter, OrderingFilter, PostTagFilter)
    permission_classes = [ActionBasedPermission]
    action_permissions = {
        IsAuthenticated: ['update', 'partial_update', 'destroy',
                           'list',
                          'create',
                          ],
        AllowAny: ['retrieve',
                   # 'list',
                   # 'create'
                   ]
    }
    # filterset_fields = ('author', 'title')
    search_fields = ('title',)
    ordering_fields = ('created',)
    ordering = ('-created',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark_post(request, pk):
    user = request.user
    user.bookmark_post(pk)
    return Response(status=200)
