from django.urls import path
from rest_framework import routers

from masters import views

app_name = 'Masters api'

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', views.MasterListView.as_view(), name='list'),
    path('<int:pk>', views.MasterRetrieveView.as_view(), name='retrieve'),
]

urlpatterns += router.urls
