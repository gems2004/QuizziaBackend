from Users.serializers.UserSerializers import UpdateUserSerializer, UserSerializer
from Users.models import Manager, Teacher, User
from rest_framework import serializers


class ManagerSerializer(serializers.Serializer):
    user = UserSerializer()
    no_of_teachers = serializers.SerializerMethodField()

    def get_no_of_teachers(self, obj):
        return Teacher.objects.filter(fk_manager_id=obj).count()

    class Meta:
        model = Manager
        fields = ["user", "no_of_teachers"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["role"] = "Manager"
        user = User.objects.create(**user_data)
        user.set_password(user_data["password"])
        user.save()
        manager = Manager.objects.create(user=user)
        manager.save()
        return manager


class UpdateManagerSerializer(serializers.Serializer):
    user = UpdateUserSerializer(partial=True, required=False)

    class Meta:
        model = Manager
        fields = ["user"]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        instance.user.username = user_data.get("username", instance.user.username)
        instance.user.password = user_data.get("password", instance.user.password)
        instance.save()
        return instance
