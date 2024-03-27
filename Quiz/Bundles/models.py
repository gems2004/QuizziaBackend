from django.db import models
from django.db import models
# Create your models here.


class Bundle(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=20,decimal_places=3)
    no_of_questions = models.IntegerField()
    no_of_quizzes = models.IntegerField()
    no_of_students = models.IntegerField()

