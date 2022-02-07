from django.urls import path
from rest_framework import routers

from registers import views

app_name = 'Registers api'

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('', views.RegisterListCreateView.as_view(), name='list_create'),
    path('<int:pk>', views.RegisterRetrieveUpdateDestroyView.as_view(), name='retrieve_update_destroy'),
    path('user', views.RegisterUserListView.as_view(), name='user_list'),
]

urlpatterns += router.urls
