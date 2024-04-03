from Users.serializers.UserSerializers import UserSerializer
from Users.models import Student, User
from rest_framework import serializers

from StudentDoQuiz.models import StudentDoQuiz
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
