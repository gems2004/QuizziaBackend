from Bundles.models import Bundle
from Bundles.serializer import BundleSerializer
from QuizMaker.Models.Questions import Questions
from QuizMaker.Models.QuizMaker import QuizMake
from StudentDoQuiz.models import StudentDoQuiz
from Users.models import Student, User, Teacher
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, source="id")
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["user_id", "username", "password", "role"]


class UpdateUserSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, source="id")
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["user_id", "username", "role"]


class StudentSerializer(serializers.ModelSerializer):
    no_of_quizzes_done = serializers.SerializerMethodField()
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = [
            "id",
            "fullname",
            "user",
            "no_of_quizzes_done",
        ]

    def get_no_of_quizzes_done(self, obj):
        return StudentDoQuiz.objects.filter(fk_student_id=obj.id).count()

    def create(self, validated_data):
        validated_data["user"]["role"] = "Student"
        user_data = validated_data.pop("user")
        user_instance = User.objects.create(**user_data)
        user_instance.set_password(user_data["password"])
        user_instance.save()
        student_instance = Student.objects.create(user=user_instance, **validated_data)
        return student_instance


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

    class Meta:
        model = Teacher
        fields = [
            "user",
            "teacher_id",
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
    fk_bundle = serializers.PrimaryKeyRelatedField(queryset=Bundle.objects.all(), required=False)

    class Meta:
        model = Teacher
        fields = [
            "user",
            "fullname",
            "subject",
            "fk_bundle",
        ]

    def update(self, instance, validated_data):
        print(validated_data)
        user_data = validated_data.pop('user')
        instance.user.username = user_data.get('username', instance.user.username)
        instance.user.password = user_data.get('password', instance.user.password)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.bundle_data = validated_data.get('fk_bundle', instance.fk_bundle)
        instance.save()
        if instance.user.username != validated_data.get('username', instance.user.username):
            token, created = Token.objects.get_or_create(user=instance.user)
            token.delete()
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        username = data.get("username")

        if Teacher.objects.filter(username=username).exists():
            return data
        else:
            raise serializers.ValidationError(
                {"error": "Please enter valid credentials"}
            )

    def save(self):
        username = self.validated_data["username"]
        password = self.validated_data["password"]
        teacher = Teacher.objects.get(username=username)
        teacher.set_password(password)
        teacher.save()
        return teacher


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user.role == "Teacher":
            teacher = Teacher.objects.get(user=user)
            token["teacher_id"] = teacher.id
        elif user.role == "Student":
            student = Student.objects.get(user=user)
            token["student_id"] = student.id
        else:
            pass
        token["role"] = user.role
        return token
