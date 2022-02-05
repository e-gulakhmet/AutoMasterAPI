from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from tokens import views

app_name = 'Users api'

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verify', TokenVerifyView.as_view(), name='token_verify'),
    path('check', views.LoginCheckView.as_view(), name='token_check_auth'),
]

urlpatterns += router.urls
