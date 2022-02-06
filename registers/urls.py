from django.urls import path, register_converter
from rest_framework import routers

from main.converters import DateConverter
from registers import views

app_name = 'Registers api'

router = routers.SimpleRouter(trailing_slash=False)

register_converter(DateConverter, 'date')

urlpatterns = [
    path('', views.RegisterListCreateView.as_view(), name='list_create'),
    path('<int:pk>', views.RegisterRetrieveUpdateDestroyView.as_view(), name='retrieve_update_destroy'),
    path('master/<int:master_pk>', views.RegisterMasterListView.as_view(), name='master_list'),
    path('master/<date:start_date>/<date:end_date>', views.RegisterFreeDateListView.as_view(), name='free_dates_list'),
]

urlpatterns += router.urls
