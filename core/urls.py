"""makeitgreener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view
from users.views import already_logined
from . import settings

schema_view = get_swagger_view(title='Pastebin API')

api_urlpatterns = [
    path('api/', include('blog.api.urls')),
    path('api/', include('chat.api.urls')),
    path('api/', include('users.api.urls')),

]

urlpatterns = [
                  path('', TemplateView.as_view(template_name='home.html'), name='home'),
                  path('logined_already', already_logined, name='already-logined'),
                  path('admin/', admin.site.urls),
                  path('', include('blog.urls')),
                  path('', include('users.urls')),
                  # path('chat/', include('chat.urls')),
                  path('swag/', schema_view),

              ] + api_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'blog.views.e_handler404'
handler500 = 'blog.views.e_handler500'
