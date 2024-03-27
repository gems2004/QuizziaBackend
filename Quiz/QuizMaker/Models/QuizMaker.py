from django.db import models
from django.urls import include
from Users.models import Teacher


class QuizMake(models.Model):
    name = models.CharField(max_length=50)
    req_time = models.CharField(max_length=10)
    quiz_token = models.CharField(max_length=8, unique=True)
    fk_teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
