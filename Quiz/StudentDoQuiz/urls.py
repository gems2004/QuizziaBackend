from django.urls import path
from .views import (
    SubmitStudentQuiz,
    StudentRecord,
    StudentRequestView,
    TeacherRequests,
    ApproveToStudent,
    DeclineToStudent,
    StartQuiz,
    StudentsOfTeacher,
    generatePdf,
)

urlpatterns = [
    path("student/submit", SubmitStudentQuiz.as_view()),
    path("student/start", StartQuiz.as_view()),
    path("student/record/<int:fk>", StudentRecord.as_view()),
    path("teacher/record/<int:pk>", StudentsOfTeacher.as_view()),
    path("teacher/record/pdf/<int:pk>", generatePdf.as_view()),
    path("student/request/", StudentRequestView.as_view()),
    path("teacher/requests/", TeacherRequests.as_view()),
    path("teacher/request/approve/<int:pk>", ApproveToStudent.as_view()),
    path("teacher/request/decline/<int:pk>", DeclineToStudent.as_view()),
]
