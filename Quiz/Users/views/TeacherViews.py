from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import Response, status

from Users.models import Teacher, User
from Users.permissions import ManagerPermissions, TeacherPermissions
from Users.serializers.TeacherSerializer import (
    RenewSubscriptionSerializer,
    TeacherSerializer,
    UpdateTeacherSerializer,
)


class RegisterTeacher(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser, ManagerPermissions]

    def post(self, request):
        try:
            request.data["fk_manager"] = request.user.manager.id or None
            serializer = TeacherSerializer(data=request.data)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            subscription = RenewSubscriptionSerializer(
                data={"teacher_id": serializer.data["teacher_id"]}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RetrieveTeacher(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = UpdateTeacherSerializer(teacher, data=request.data, many=False)
            subscription = RenewSubscriptionSerializer(data={"teacher_id": teacher.id})
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.update(teacher, request.data)
            if subscription.is_valid():
                subscription.save()
            else:
                return Response(subscription.errors)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, instance, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            user = User.objects.get(pk=teacher.user.id)
            user.delete()
            return Response("deleted successfully", status.HTTP_200_OK)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_404_NOT_FOUND)


class GetAllTeachers(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            teachers = Teacher.objects.all()
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_404_NOT_FOUND)


class RenewSubscription(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        try:
            serializer = RenewSubscriptionSerializer(data=request.data)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.save())
        else:
            return Response(serializer.errors)
