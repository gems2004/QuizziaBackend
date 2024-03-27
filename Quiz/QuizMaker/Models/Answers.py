from django.db import models
from .Questions import Questions


class Answers(models.Model):
    fk_question_id = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
