from rest_framework import serializers
from Users.models import User, Teacher, Student
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
