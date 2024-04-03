from QuizMaker.Models.Answers import Answers
from QuizMaker.Models.Questions import Questions
from QuizMaker.Models.QuizMaker import QuizMake
from QuizMaker.serializer import QuizSerializer
from Users.models import Student
from Users.serializers.StudentSerializer import StudentSerializer
from rest_framework import serializers

from .models import StudentDoQuiz, ChosenAnswer, StudentRequest


class ChosenAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenAnswer
        fields = ["fk_question_id", "fk_answer_id"]
        read_only_fields = ["id"]


class StudentDoQuizSerializer(serializers.ModelSerializer):
    chosen = ChosenAnswerSerializer(many=True)
    fk_student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects)
    # fk_quiz_id = serializers.PrimaryKeyRelatedField(queryset=QuizMake.objects)
    student = StudentSerializer(source="fk_student_id", read_only=True)
    student_did_quiz = serializers.BooleanField(read_only=True)

    # quiz = QuizSerializer(source="fk_quiz_id", read_only=True)

    class Meta:
        model = StudentDoQuiz
        fields = [
            "id",
            "fk_quiz_id",
            "fk_student_id",
            "student",
            "student_did_quiz",
            "grade",
            "time_spent",
            "chosen",
        ]
        read_only_fields = ["grade", "student_did_quiz"]

    def create(self, validated_data):
        chosen_data = validated_data.pop("chosen")
        student_do = StudentDoQuiz.objects.create(**validated_data)
        fk_quiz_id = validated_data["fk_quiz_id"]
        student_do.student_did_quiz = True
        questions = Questions.objects.filter(fk_quiz_id=fk_quiz_id).count()
        student_do.save()
        score = 0
        for chosen in chosen_data:
            print(chosen["fk_question_id"].id)
            fk_question_id = chosen["fk_question_id"]
            fk_answer_id = chosen["fk_answer_id"]
            chosen_object = ChosenAnswer.objects.create(
                fk_question_id=fk_question_id, fk_answer_id=fk_answer_id
            )
            answer = Answers.objects.get(pk=fk_answer_id.id)
            if answer.is_correct:
                score += 1
            chosen_object.save()
            final_grade = (score * 100) / questions
            student_do.grade = final_grade
            student_do.chosen.add(chosen_object)
            student_do.save()
        return student_do


class StudentRequestSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects, many=False, write_only=True
    )
    quiz = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    student_data = StudentSerializer(source="student", many=False, read_only=True)
    quiz_data = QuizSerializer(source="quiz", many=False, read_only=True)
    quiz_token = serializers.CharField(write_only=True)
    approved = serializers.BooleanField(required=False)
    class Meta:
        model = StudentRequest
        fields = [
            "id",
            "created_at",
            "student_data",
            "student",
            "quiz",
            "quiz_data",
            "quiz_token",
            "approved",
        ]

    def create(self, validated_data):
        token = validated_data.get("quiz_token")
        student = validated_data.get("student")
        try:
            quiz = QuizMake.objects.get(quiz_token=token)
        except QuizMake.DoesNotExist:
            raise serializers.ValidationError("Invalid token")
        instance = StudentRequest.objects.create(
            student=student,
            quiz=quiz,
        )

        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["quiz_data"].pop("questions")
        return response
