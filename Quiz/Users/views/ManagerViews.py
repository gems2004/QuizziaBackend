from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import Response, status
from Quiz.Users.serializers.TeacherSerializer import TeacherSerializer
from Users.serializers.ManagerSerializer import (
    ManagerSerializer,
    UpdateManagerSerializer,
)
from Users.models import Manager, Student, Teacher


class CreateManager(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        try:
            serializer = ManagerSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllManagers(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self):
        try:
            managers = Manager.objects.all()
            serializer = ManagerSerializer(managers, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_404_NOT_FOUND)


class RetrieveManager(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, pk):
        try:
            manager = Manager.get(pk=pk)
            serializer = ManagerSerializer(manager, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            manager = Manager.objects.get(pk=pk)
            serializer = UpdateManagerSerializer(instance=manager, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return (str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, pk):
        try:
            manager = Manager.objects.get(pk=pk)
            manager.delete()
            return Response("deleted successfully", status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)


class TeachersOfManager(APIView):
    def get(self, request, pk):
        try:
            teachers = Teacher.objects.filter(fk_manager_id=pk)
            serializer = TeacherSerializer(teachers, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status.HTTP_404_NOT_FOUND)
