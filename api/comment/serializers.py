from rest_framework import serializers

from .models import Comment, CommentVote


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment_text', 'created_at', 'updated_at')


class CommentVoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommentVote
        fields = ('id', 'vote_type', 'created_at', 'updated_at')
