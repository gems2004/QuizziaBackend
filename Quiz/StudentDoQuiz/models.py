from QuizMaker.Models.Answers import Answers
from QuizMaker.Models.Questions import Questions
from QuizMaker.Models.QuizMaker import QuizMake
from Users.models import Student
from django.db import models


# Create your models here.


class ChosenAnswer(models.Model):
    fk_question_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    fk_answer_id = models.ForeignKey(Answers, on_delete=models.CASCADE)


class StudentDoQuiz(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    fk_quiz_id = models.ForeignKey(QuizMake, on_delete=models.PROTECT)
    fk_student_id = models.ForeignKey(Student, on_delete=models.PROTECT)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    time_spent = models.DateTimeField()
    student_did_quiz = models.BooleanField(default=False)
    chosen = models.ManyToManyField(ChosenAnswer)


class StudentRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizMake, on_delete=models.CASCADE)
    approved = models.BooleanField(null=True)
