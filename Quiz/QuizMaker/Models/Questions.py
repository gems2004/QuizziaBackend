from django.db import models
from .QuizMaker import QuizMake

class Questions(models.Model):
    fk_quiz_id = models.ForeignKey(QuizMake, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    image = models.ImageField(null=True)
