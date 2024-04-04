from rest_framework import serializers

from Bundles.models import Bundle
from Users.models import Teacher
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
        print(req_time, current_time)
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

        questions_data = validated_data.get("questions", [])
        instance.questions.all().delete()
        for question_data in questions_data:
            answers_data = question_data.pop("answers", [])
            question = Questions.objects.create(fk_quiz_id=instance, **question_data)
            for answer_data in answers_data:
                Answers.objects.create(fk_question_id=question, **answer_data)

        instance.save()
        return instance
    
    def validate(self, attrs):
        no_of_quizzes = 0
        no_of_questions = 0
        get_quizzes = QuizMake.objects.filter(fk_teacher_id=attrs['fk_teacher_id'].id)
        get_no_of_quizzes = QuizMake.objects.filter(fk_teacher_id=attrs['fk_teacher_id'].id).count()
        no_of_quizzes = get_no_of_quizzes
        get_user_data = Teacher.objects.get(pk=attrs['fk_teacher_id'].id)
        get_bundle_data = Bundle.objects.get(pk=get_user_data.fk_bundle.id)
        for quiz in get_quizzes:
            get_questions = Questions.objects.filter(fk_quiz_id=quiz.id).count()
            no_of_questions += get_questions
        print(no_of_quizzes, no_of_questions, get_bundle_data.no_of_quizzes, get_bundle_data.no_of_questions)
        if no_of_quizzes >= get_bundle_data.no_of_quizzes or no_of_questions >= get_bundle_data.no_of_questions:
            raise serializers.ValidationError("teacher exceeded limits please upgrade your bundle")
        else:
            return attrs
    