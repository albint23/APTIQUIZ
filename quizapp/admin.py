from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserImages)
admin.site.register(Quizzes)
admin.site.register(Questions)
admin.site.register(UserResponse)
admin.site.register(QuizSession)