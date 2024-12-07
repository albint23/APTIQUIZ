from django.urls import path
from . import views

urlpatterns = [
    path('admin_dash/', views.admin_dash, name='admin_dash'),
    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('edit_quiz/<int:quiz_id>', views.edit_quiz, name='edit_quiz'),
    path('delete_quiz/<int:quiz_id>', views.delete_quiz, name='delete_quiz'),
    path('add_questions/<int:quiz_id>', views.add_questions, name='add_questions'),
    path('edit_questions/<int:quiz_id>', views.edit_questions, name='edit_questions'),
    path('view_users/', views.view_users, name='view_users'),
    path('remove_user/<int:user_id>', views.remove_user, name='remove_user'),
    path('view_results/', views.view_results, name='view_results'),
]
