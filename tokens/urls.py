from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from tokens import views

app_name = 'Tokens api'

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', views.TokenObtainPairView.as_view(), name='obtain_pair'),
    path('refresh', views.TokenRefreshView.as_view(), name='refresh'),
    path('verify', TokenVerifyView.as_view(), name='verify'),
    path('check', views.LoginCheckView.as_view(), name='check_auth'),
]

urlpatterns += router.urls
