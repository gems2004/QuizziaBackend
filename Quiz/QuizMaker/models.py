from django.db import models
from django.urls import include

# Create your models here.
include('QuizMaker.Models.QuizMaker')
include('QuizMaker.Models.Questions')
include('QuizMaker.Models.Answers')


