from django.urls import include, path

from .views import home

urlpatterns = [
    path('', home),
    path('user/', include('api.user.urls')),
    path('question/', include('api.question.urls')),
    path('answer/', include('api.answer.urls')),
    path('comment/', include('api.comment.urls')),
]
