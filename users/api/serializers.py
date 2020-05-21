from rest_framework import serializers
from users.models import User


class OtherUserSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'is_friend')
        read_only_fields = ['username']

    def get_is_friend(self, obj):
        request = self.context['request']
        value = 'false'
        user = request.user
        if user.is_anonymous:
            return 'anonymous'
        if obj.pk == user.pk:
            value = 'null'
        elif obj.pk in request.user.follow.all().values_list('id', flat=True):
            value = 'true'
        return value
