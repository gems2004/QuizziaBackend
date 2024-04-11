from datetime import datetime, timedelta
from rest_framework import serializers
from Users.models import Teacher, User
from Bundles.serializer import BundleSerializer
from Users.serializers.UserSerializers import UserSerializer, UpdateUserSerializer
from QuizMaker.Models.QuizMaker import QuizMake
from QuizMaker.Models.Questions import Questions
from Bundles.models import Bundle


class TeacherSerializer(serializers.ModelSerializer):
    teacher_id = serializers.PrimaryKeyRelatedField(read_only=True, source="id")
    user = UserSerializer(many=False)
    fk_bundle = serializers.PrimaryKeyRelatedField(
        queryset=Bundle.objects, required=False, write_only=True
    )
    bundle_data = BundleSerializer(source="fk_bundle", read_only=True)
    no_of_quizzes = serializers.SerializerMethodField()
    no_of_questions = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(read_only=True)
    fk_manager = serializers.IntegerField(read_only=True)

    class Meta:
        model = Teacher
        fields = [
            "user",
            "teacher_id",
            "fk_manager",
            "fullname",
            "subject",
            "is_subscribed",
            "no_of_quizzes",
            "no_of_questions",
            "bundle_data",
            "fk_bundle",
        ]

    # def get_no_of_students(self, obj):
    #     return Student.objects.filter(fk_teacher=obj.id).count()

    def get_no_of_quizzes(self, obj):
        return QuizMake.objects.filter(fk_teacher_id=obj.id).count()

    def get_no_of_questions(self, obj):
        quizzes = QuizMake.objects.filter(fk_teacher_id=obj.id)
        count = 0
        for quiz in quizzes:
            questions = Questions.objects.filter(fk_quiz_id=quiz.id).count()
            count += questions
        return count

    def create(self, validated_data):
        bundle_expiry = validated_data.get("bundle_expiry", None)
        validated_data["bundle_expiry"] = bundle_expiry
        validated_data["user"]["role"] = "Teacher"
        user_data = validated_data.pop("user")
        user_instance = User.objects.create(**user_data)
        user_instance.set_password(user_data["password"])
        user_instance.save()
        teacher_instance = Teacher.objects.create(user=user_instance, **validated_data)
        if teacher_instance.fk_bundle.name == "free":
            teacher_instance.bundle_expiry = None
            teacher_instance.save()
        else:
            current_time = datetime.now()
            teacher_instance.bundle_expiry = current_time + timedelta(days=35)
            teacher_instance.is_subscribed = True
            teacher_instance.save()
        return teacher_instance


class RenewSubscriptionSerializer(serializers.Serializer):
    teacher_id = serializers.IntegerField()

    def save(self):
        teacher_id = self.validated_data["teacher_id"]
        teacher = Teacher.objects.get(id=teacher_id)
        if teacher.fk_bundle.name == "free":
            raise serializers.ValidationError(
                {"error": "free bundle cannot be renewed"}
            )
        else:
            current_time = datetime.now()
            teacher.bundle_expiry = current_time + timedelta(days=35)
            teacher.is_subscribed = True
            teacher.save()

        return {"success": "Subscription renewed successfully"}


class UpdateTeacherSerializer(serializers.Serializer):
    user = UpdateUserSerializer(required=False, partial=True)
    fullname = serializers.CharField(required=False)
    subject = serializers.CharField(required=False)
    fk_bundle = serializers.PrimaryKeyRelatedField(
        queryset=Bundle.objects.all(), required=False, write_only=True
    )
    fk_bundle_id = serializers.IntegerField(required=False)
    fk_manager = serializers.IntegerField(required=False)

    class Meta:
        model = Teacher
        fields = ["user", "fullname", "subject", "fk_bundle_id", "fk_manager"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        instance.user.username = user_data.get("username", instance.user.username)
        instance.user.password = user_data.get("password", instance.user.password)
        instance.fullname = validated_data.get("fullname", instance.fullname)
        instance.subject = validated_data.get("subject", instance.subject)
        instance.fk_bundle_id = validated_data.get(
            "fk_bundle_id", instance.fk_bundle_id
        )
        instance.fk_manager = validated_data.get("fk_manager", instance.fk_manager)
        instance.save()
        return instance
