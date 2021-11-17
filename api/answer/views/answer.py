from django.http import JsonResponse
from django.db.models import Q
from django.utils.decorators import decorator_from_middleware, decorator_from_middleware_with_args
from rest_framework.decorators import api_view
from rest_framework import status
from api.constants.ask_type_constants import LIMITED, PUBLIC
from ..serializers import AnswerSerializer
from ..models import Answer
from ...question.models import Question
from ...user.models import Follow
from django.views.decorators.csrf import csrf_exempt
import json
from ...middleware.auth_strategy import AuthStrategyMiddleware

# Create your views here.


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware_with_args(AuthStrategyMiddleware)(False)
def get_all_answers(request):
    # In order to get the votes as well, required query is
    # SELECT *, (SELECT COUNT(*) FROM 'answer_answervote'
    #            WHERE answer_id = answer_answer.id) as up_votes
    # FROM 'answer_answer';
    try:
        if request.user is None:
            # If no user is logged, we fetch all answers whose questions are public
            answers = Answer.objects.filter(question__ask_type=PUBLIC).all()
        else:
            # If user is logged, we fetch only those answers whose questions are limited and which are posted by some followee user to our logged user
            answers_to_public_questions = Answer.objects.filter(
                question__ask_type=PUBLIC).all()
            followees = Follow.objects.filter(
                follower__id=request.user.id).values('id')
            answers_to_limited_questions = Answer.objects.filter(
                Q(question__owner__id__in=followees) | Q(question__owner__id=request.user.id)).all()
            #  combining both of the answers
            answers = (answers_to_public_questions |
                       answers_to_limited_questions)
        return JsonResponse({
            'success': True,
            'message': 'All answers of the portal',
            'answers': AnswerSerializer(answers, many=True).data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
@decorator_from_middleware_with_args(AuthStrategyMiddleware)(False)
def get_answers_to_particular_question(request, question_id):
    try:
        the_question = Question.objects.get(id=question_id)
        if request.user is None:
            if the_question.ask_type == LIMITED:
                return JsonResponse({
                    'success': False,
                    'message': 'Access blocked to unauthorized user'
                }, status=status.HTTP_401_UNAUTHORIZED)
            answers = Answer.objects.filter(question__id=question_id).all()
        else:
            if not Follow.objects.filter(followee=the_question.owner.id, follower=request.user.id).exists() and the_question.ask_type == LIMITED and the_question.owner.id != request.user.id:
                return JsonResponse({
                    'success': False,
                    'message': 'Question is limited and can only be accessed by followers of the owner'
                }, status=status.HTTP_401_UNAUTHORIZED)
            answers = Answer.objects.filter(question__id=question_id).all()
        return JsonResponse({
            'success': True,
            'message': f"All answers of particular question with id {question_id}",
            'answers': AnswerSerializer(answers, many=True).data
        }, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Question does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Follow.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Logged user not eligible to view answers to this question'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def create_new_answer(request, question_id):
    data = json.loads(request.body)
    try:
        answer = data['answer']
        question = Question.objects.get(id=question_id)
        new_answer = Answer.objects.create(
            answer=answer, question=question, owner=request.user)
        return JsonResponse({
            'success': True,
            'message': 'Successfully created new answer',
            'answer': AnswerSerializer(new_answer).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Answer body parameter not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Question.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Question with given id does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_answer(request, answer_id):
    data = json.loads(request.body)
    try:
        existing_answer = Answer.objects.get(
            id=answer_id, owner__id=request.user.id)
        if 'answer' in data:
            existing_answer.answer = data['answer']
        existing_answer.save()
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated answer',
            'question': AnswerSerializer(existing_answer).data
        }, status=status.HTTP_200_OK)
    except Answer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Answer does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def delete_existing_answer(request, answer_id):
    try:
        existing_answer = Answer.objects.get(
            id=answer_id, owner__id=request.user.id)
        existing_answer.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted answer',
        }, status=status.HTTP_200_OK)
    except Answer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Answer does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)
