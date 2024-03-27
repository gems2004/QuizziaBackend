from rest_framework.views import APIView,Response,status
from Users.models import Teacher
from .Models.QuizMaker import QuizMake
from .serializer import QuizSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from Users.permissions import TeacherPermissions

# Create your views here.

class QuizMakerAPIView(APIView):
    authentication_classes = [TokenAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def post(self,request):
        quiz = request.data
        serializer = QuizSerializer(data=quiz, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
class QuizAPIView(APIView):
    authentication_classes = [TokenAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, fk):
        teacher = Teacher.objects.get(pk=fk)
        quizes = QuizMake.objects.filter(fk_teacher_id = teacher.pk)
        serializer = QuizSerializer(quizes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class SpecificQuiz(APIView):
    authentication_classes = [TokenAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, pk):
        try:
            quiz = QuizMake.objects.get(pk = pk)
            serializer = QuizSerializer(quiz)
        except:
            return Response("not found", status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status.HTTP_200_OK)
    def patch(self, request, pk):
        quiz = QuizMake.objects.get(pk=pk)

        serializer = QuizSerializer(quiz, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):

        try:
            quiz = QuizMake.objects.get(pk = pk)
            quiz.delete()
        except:
            return Response("not found", status.HTTP_404_NOT_FOUND)

        return Response('deleted successfully', status.HTTP_200_OK)
