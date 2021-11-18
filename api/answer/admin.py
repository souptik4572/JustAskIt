from django.contrib import admin

from .models import Answer, AnswerVote

# Register your models here.
admin.site.register(Answer)
admin.site.register(AnswerVote)
