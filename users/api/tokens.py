from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class TokenCreate(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        return res


class TokenRefresh(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        return res
