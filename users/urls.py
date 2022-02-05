from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from rest_framework import routers

from users import views

app_name = 'Users api'

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = [
    # path('register', views.UserCreateView.as_view(), name='register'),
    # # Password
    # path('password/change', views.ChangePasswordView.as_view(), name='change_password'),
    # path('password/reset', views.RequestResetPasswordView.as_view(), name='request_reset_password'),
    # path('password/reset/check', views.CheckResetCodeView.as_view(), name='check_password_reset_code'),
    # path('password/new', views.ResetPasswordView.as_view(), name='reset_password'),
    # # User
    # path('me', views.UserRetrieveUpdateView.as_view(), name='me'),
    # path('settings', views.AccountSettingsView.as_view(), name='settings'),
    # path('become_provider', views.BecomeProviderView.as_view(), name='become_provider'),
    # path('list', views.UsersListView.as_view(), name='users_list'),
    # path('id/<int:pk>', views.UserGetByIdView.as_view(), name='by_id'),
    # path('username/<str:username>', views.UserRetrieveByUsernameView.as_view(), name='by_username'),
]

urlpatterns += router.urls