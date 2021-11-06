from django.urls import path
from .views.user import register_end_user, login_user, get_user_profile, edit_user_profile, request_password_reset, update_password

urlpatterns = [
    path('register/', register_end_user, name='api.register_end_user'),
    path('login/', login_user, name='api.login_user'),
    path('profile/', get_user_profile, name='api.get_user_profile'),
    path('edit-profile/', edit_user_profile, name='api.edit_user_profile'),
    path('request-password-reset/', request_password_reset,
         name='api.request_password_reset'),
    path('update-password/', update_password,
         name='api.update_password'),
]
