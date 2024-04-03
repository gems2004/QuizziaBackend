from Users.models import Student
from Users.permissions import (
    TeacherPermissions,
    StudentPermissions,
    TeacherApprovedToStudent,
)
from Users.serializers import StudentSerializer
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import StudentDoQuiz, StudentRequest
from .serializer import (
    StudentDoQuizSerializer,
    StudentRequestSerializer,
)


# Create your views here.
class SubmitStudentQuiz(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def post(self, request):
        serializer = StudentDoQuizSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class StudentRecord(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, fk):
        try:
            student_data = Student.objects.get(pk=fk)
            serializer_student = StudentSerializer(student_data)
            student_do_quiz = StudentDoQuiz.objects.filter(fk_student_id=fk)
            serializer = StudentDoQuizSerializer(student_do_quiz, many=True)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_404_NOT_FOUND)
        return Response(
            {"student": serializer_student.data, "data": serializer.data},
            status.HTTP_200_OK,
        )

    def delete(self, request, fk):
        try:
            student_do_quiz = StudentDoQuiz.objects.get(pk=fk)
            student_do_quiz.delete()
        except Exception as e:
            return Response({"error": str(e)})
        return Response("deleted successfully", status.HTTP_200_OK)


class StudentRequestView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, StudentPermissions | IsAdminUser]

    def get(self, request):

        student = request.user.student
        requests = StudentRequest.objects.filter(student=student)
        serializer = StudentRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['student'] = request.user.student.id
        serializer = StudentRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class StudentsOfTeacher(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, pk):
        quiz = StudentDoQuiz.objects.filter(fk_quiz_id=pk)
        try:
            serializer = StudentDoQuizSerializer(quiz, many=True)
        except Exception as e:
            return Response(str(e), status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)


class TeacherRequests(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request):
        try:
            teacher = request.user.teacher
            requests = StudentRequest.objects.filter(quiz__fk_teacher_id=teacher.id, approved=None)
            serializer = StudentRequestSerializer(requests, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e))


class ApproveToStudent(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def post(self, request, pk):
        student_request = StudentRequest.objects.get(pk=pk)
        try:
            serializer = StudentRequestSerializer(
                instance=student_request, data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:

                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e))



class StartQuiz(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [
        IsAuthenticated,
        (StudentPermissions & TeacherApprovedToStudent) | IsAdminUser,
    ]

    def post(self, request):
        return Response("validated successfully")


class generatePdf(APIView):
    def get(self, request, pk):
        def generate_pdf(response, quiz_data):
            pdf = canvas.Canvas(response, pagesize=letter)

            pdf.setFont("Helvetica", 12)

            pdf.drawCentredString(300, 750, "Quiz Report")

            header_data = ["Quiz", "Student", "Grade"]
            for i, header in enumerate(header_data):
                pdf.drawString(100 + i * 120, 730, header)

            y_position = 710
            for entry in quiz_data:
                pdf.drawString(100, y_position, str(entry.fk_quiz_id.name))
                pdf.drawString(220, y_position, str(entry.fk_student_id.fullname))
                pdf.drawString(340, y_position, str(entry.grade))
                y_position -= 20

            pdf.line(100, y_position, 500, y_position)

            pdf.save()

            return response

        quiz_data = StudentDoQuiz.objects.filter(fk_quiz_id=pk)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="quiz_report.pdf"'
        return generate_pdf(response, quiz_data)
