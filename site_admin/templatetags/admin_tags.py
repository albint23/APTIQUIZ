from django import template
from quizapp.models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

register = template.Library()

@register.filter
def is_questions(quiz_id):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    question_exists = Questions.objects.filter(quiz=quiz).exists()
    return question_exists

@register.filter
def get_questions(quiz_id):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    questions = Questions.objects.filter(quiz=quiz)
    return questions

@register.filter
def get_sessions(quiz_id):
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    sessions = QuizSession.objects.filter(quiz=quiz)
    return sessions

@register.filter
def attended_quizzes(user_id):
    user = get_object_or_404(User, pk=user_id)
    quizzes = Quizzes.objects.filter(attendees=user)
    return quizzes

@register.filter
def find_session(user_id, quiz_id):
    user = get_object_or_404(User, pk=user_id)
    quiz = get_object_or_404(Quizzes, pk=quiz_id)
    session = QuizSession.objects.get(user=user, quiz=quiz)
    return session

@register.filter
def hash(id):
    hashed_id = urlsafe_base64_encode(force_bytes(id))
    return hashed_id

@register.filter
def add_class(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    return value.as_widget(attrs={'class': f'{css_classes} {arg}'})