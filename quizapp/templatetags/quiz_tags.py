from django import template
from quizapp.models import *
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter
def get_user_response(user_responses_dict, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        user_response = UserResponse.objects.get(question=question)
        return user_response
    except UserResponse.DoesNotExist:
        return None

@register.filter
def format_duration(duration):
    minutes, seconds = divmod(duration.seconds, 60)
    return f"{minutes} min {seconds} seconds"


@register.filter
def get_quizzes(category, user_id):
    user = get_object_or_404(User, pk=user_id)
    sessions = QuizSession.objects.filter(user=user, quiz__category=category)
    return sessions

@register.filter
def find_total(mark, tot_questions):
    total_marks = mark * tot_questions
    return total_marks

@register.filter
def have_questions(quiz_id):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    if Questions.objects.filter(quiz=quiz).exists():
        return True
    else:
        return False