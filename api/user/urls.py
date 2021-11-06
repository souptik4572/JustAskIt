from django.urls import path
from .views import register_end_user, login_user, get_user_profile

urlpatterns = [
    path('register/', register_end_user, name='api.register_end_user'),
    path('login/', login_user, name='api.login_user'),
    path('profile/', get_user_profile, name='api.get_user_profile'),
]
