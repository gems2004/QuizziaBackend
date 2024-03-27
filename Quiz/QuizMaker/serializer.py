from rest_framework import serializers
from .Models.QuizMaker import QuizMake
from .Models.Answers import Answers
from .Models.Questions import Questions
import string, secrets


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ["id", "answer", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Questions
        fields = ["id", "question", "description", "image", "answers"]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    quiz_token = serializers.CharField(read_only=True)

    class Meta:
        model = QuizMake
        fields = ["id", "name", "req_time", "quiz_token", "fk_teacher_id", "questions"]

    def token_generator(self):
        characters = string.ascii_letters + string.digits
        token = "".join(secrets.choice(characters) for _ in range(8))
        return token

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")

        quiz = QuizMake.objects.create(
            name=validated_data["name"],
            req_time=validated_data["req_time"],
            fk_teacher_id=validated_data["fk_teacher_id"],
            quiz_token=self.token_generator(),
        )
        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Questions.objects.create(fk_quiz_id=quiz, **question_data)
            for answer_data in answers_data:
                Answers.objects.create(fk_question_id=question, **answer_data)
        return quiz

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.req_time = validated_data.get("req_time", instance.req_time)
        instance.fk_teacher_id = validated_data.get(
            "fk_teacher_id", instance.fk_teacher_id
        )

        # Update questions
        questions_data = validated_data.get("questions", [])
        instance.questions.all().delete()
        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question = Questions.objects.create(fk_quiz_id=instance, **question_data)
            for answer_data in answers_data:
                Answers.objects.create(fk_question_id=question, **answer_data)

        instance.save()
        return instance
