from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles', null=True, blank=True)
    
    def __str__(self):
        return str(self.user)

class Quizzes(models.Model):
    
    Categories = [
        ('qa', 'Quantitative Aptitude'),
        ('lr', 'Logical Reasoning'),
        ('vb', 'Verbal Ability'),
    ]
    
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30, choices=Categories, default='qa')
    total_questions = models.IntegerField()
    marks_for_each = models.IntegerField()
    time_limit = models.FloatField(default=0)
    attendees = models.ManyToManyField(User, related_name='attended_quizzes', blank=True)
    
    def __str__(self):
        return f'{self.category} - {self.name}'

class Questions(models.Model):
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50, null=True)
    question = models.TextField(blank=False, null=True)
    image = models.ImageField(upload_to='quiz_imgs', null=True, blank=True)
    option_1 = models.CharField(max_length=255, null=True)
    option_2 = models.CharField(max_length=255, null=True)
    option_3 = models.CharField(max_length=255, null=True)
    option_4 = models.CharField(max_length=255, null=True)
    answer = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.question

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.user)

class QuizSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    score = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate duration before saving
        if self.end_time and self.start_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user} - {self.quiz}'