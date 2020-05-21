from rest_framework import serializers
from taggit.models import Tag
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from blog.models import Post
from users.api.serializers import OtherUserSerializer


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    author = OtherUserSerializer(required=False, read_only=True)
    created = serializers.DateTimeField(format="%a, %b %Y", required=False)
    marked = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'tags', 'text', 'created', 'marked', 'main_img')

    def get_marked(self, obj):
        if self.context['request'].user in obj.added.all():
            return 'true'
        return 'false'

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(
            **validated_data,
            author=user
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
