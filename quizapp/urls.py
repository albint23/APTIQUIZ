from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('reset_password/<id>/<token>/', views.reset_password, name='reset_password'),
    path('user_dash/', views.user_dash, name='user_dash'),
    path('signout/', views.signout, name='signout'),
    path('view_quizzes/<cat>/', views.view_quizzes, name='view_quizzes'),
    path('attend_quiz/<quiz_id>/<str:mode>/', views.attend_quiz, name='attend_quiz'),
    path('quiz/<int:quiz_id>/navigate/<int:question_number>/', views.navigate_question, name='navigate_question'),
    path('finish_quiz/<int:quiz_id>/', views.finish_quiz, name='finish_quiz'),
    path('view_result/<quiz_id>/<user_id>/', views.view_result, name='view_result'),
    path('profile/', views.profile, name='profile'),
]
