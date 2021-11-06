from django.urls import path
from .views import register_end_user

urlpatterns = [
    path('register/', register_end_user, name='api.register_end_user')
]
