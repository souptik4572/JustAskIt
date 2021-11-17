from django.urls import path
from .views import create_new_comment, edit_existing_comment, delete_existing_comment, get_all_comments_to_particular_answer

urlpatterns = [
    path('to-answer/<int:answer_id>/', get_all_comments_to_particular_answer,
         name='api.get_all_comments_to_particular_answer'),
    path('new/to-answer/<int:answer_id>',
         create_new_comment, name='api.create_new_comment'),
    path('new/to-comment/<int:answer_id>',
         create_new_comment, name='api.create_new_comment'),
    path('<int:comment_id>/edit/', edit_existing_comment,
         name='api.edit_existing_comment'),
    path('<int:comment_id>/delete/', delete_existing_comment,
         name='api.delete_existing_comment'),
]
