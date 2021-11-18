from django.contrib import admin

from .models import Comment, CommentVote

# Register your models here.

admin.site.register(Comment)
admin.site.register(CommentVote)
