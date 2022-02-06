from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
   openapi.Info(
      title="AutoMasterAPI",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


class HealthCheckView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(responses={200: ''})
    def get(self, request):
        return Response(data='OK', status=status.HTTP_200_OK)


urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    # Health check
    path('health', HealthCheckView.as_view()),
    # Web API automatic documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Web API
    path('token/', include('tokens.urls', namespace='tokens')),
    path('user/', include('users.urls', namespace='users')),
    path('master/', include('masters.urls', namespace='masters')),
    path('register/', include('registers.urls', namespace='registers')),
] + static(settings.MEDIA_PATH, document_root=settings.MEDIA_ROOT)
