from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import Response, status

from Users.models import Student, User
from Users.permissions import TeacherPermissions
from Users.serializers.StudentSerializer import StudentSerializer


class RegisterStudent(APIView):

    def post(self, request):
        try:
            serializer = StudentSerializer(data=request.data)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class Students(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, fk):
        try:
            students = Student.objects.filter(fk_teacher=fk)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_404_NOT_FOUND)


class RetrieveStudent(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            user = User.objects.get(pk=student.user.id)
            user.delete()
            return Response("deleted successfully", status.HTTP_200_OK)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_404_NOT_FOUND)


class GetAllStudents(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_404_NOT_FOUND)
