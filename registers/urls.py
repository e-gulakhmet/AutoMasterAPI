from django.urls import path
from rest_framework import routers

from registers import views

app_name = 'Registers api'

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('<int:master_pk>', views.RegisterCreateView.as_view(), name='create'),
    # path('me', views.UserRetrieveUpdateView.as_view(), name='me'),
    # # Password
    # path('password/change', views.ChangePasswordView.as_view(), name='change_password'),
]

urlpatterns += router.urls
