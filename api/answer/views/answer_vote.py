import json

from api.constants.vote_type_constants import DOWN_VOTE, UP_VOTE
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import (decorator_from_middleware,
                                     decorator_from_middleware_with_args)
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view

from ...middleware.auth_strategy import AuthStrategyMiddleware
from ..models import Answer, AnswerVote
from ..serializers import AnswerVoteSerializer

# Create your views here.


@csrf_exempt
@api_view(['PUT', 'DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def vote_an_answer(request, answer_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
    try:
        if request.method == 'PUT':
            if data['vote_type'] not in (UP_VOTE, DOWN_VOTE):
                return JsonResponse({
                    'success': False,
                    'message': 'Vote type is not valid'
                }, status=status.HTTP_400_BAD_REQUEST)
            answer_vote = AnswerVote.objects.filter(
                answer__id=answer_id, voter__id=request.user.id).first()
            if not answer_vote:
                answer = Answer.objects.get(id=answer_id)
                if answer.owner.id == request.user.id:
                    return JsonResponse({
                        'success': False,
                        'message': 'Owner of the answer cannot vote their own answer'
                    }, status=status.HTTP_403_FORBIDDEN)
                answer_vote = AnswerVote.objects.create(
                    answer=answer, voter=request.user)
            answer_vote.vote_type = data['vote_type']
            answer_vote.save()
            return JsonResponse({
                'success': True,
                'message': f"Successfully {data['vote_type']} voted the answer",
                'answer_vote': AnswerVoteSerializer(answer_vote).data
            }, status=status.HTTP_201_CREATED)
        else:
            answer_vote = AnswerVote.objects.get(
                answer__id=answer_id, voter__id=request.user.id)
            answer_vote.delete()
            return JsonResponse({
                'success': False,
                'message': 'Un voted the given answer'
            }, status=status.HTTP_200_OK)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Vote type parameter not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Answer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Answer does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except AnswerVote.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'The vote does not exist to the answer'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
