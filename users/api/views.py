from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = OtherUserSerializer
#     pagination_class = MyPaginator
    # filter_backends = (SearchFilter, OrderingFilter, PostTagFilter)
    # filterset_fields = ('author', 'title')
    # search_fields = ('title',)
    # ordering_fields = ('created',)
    # ordering = ('-created',)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, pk):
    user = request.user
    user.follow_user(pk)
    return Response (status=200)