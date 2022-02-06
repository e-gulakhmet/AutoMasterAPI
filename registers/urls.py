from django.urls import path
from rest_framework import routers

from registers import views

app_name = 'Registers api'

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('create/<int:master_pk>', views.RegisterCreateView.as_view(), name='create'),
    path('<int:pk>', views.RegisterRetrieveUpdateDestroyView.as_view(), name='retrieve_update_destroy'),
]

urlpatterns += router.urls
