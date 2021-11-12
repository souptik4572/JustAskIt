from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home),
    path('user/', include('api.user.urls')),
    path('question/', include('api.question.urls')),
    path('answer/', include('api.answer.urls')),
]
