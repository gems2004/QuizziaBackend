from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Teacher, Student, User
from .permissions import TeacherPermissions
from .serializers.TeacherSerializer import TeacherSerializer, UpdateTeacherSerializer, RenewSubscriptionSerializer
from .serializers.StudentSerializer import StudentSerializer
from .serializers.UserSerializers import  ResetPasswordSerializer

# Create your views here.


class RegisterTeacher(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        try:
            serializer = TeacherSerializer(data=request.data)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            subscription = RenewSubscriptionSerializer(data={'teacher_id':serializer.data['teacher_id']})
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)        



class Logout(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "logged out"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            subscription = RenewSubscriptionSerializer(data={'teacher_id': teacher.id})
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


class resetpassword(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def post(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
        except Exception as e:
            return Response({"err": str(e)}, status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


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
