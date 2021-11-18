from api.constants.vote_type_constants import UP_VOTE, VOTE_TYPES
from django.db import models

from ..answer.models import Answer
from ..user.models import EndUser

# Create your models here.


class Comment(models.Model):
    owner = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='referenced_comment')
    comment_text = models.CharField(max_length=2500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.comment_text[:10]}"


class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    voter = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=5, choices=VOTE_TYPES, default=UP_VOTE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} for answer {self.comment.id}"
