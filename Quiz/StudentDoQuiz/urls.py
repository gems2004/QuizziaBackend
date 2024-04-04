from django.urls import path
from .views import (
    SubmitStudentQuiz,
    StudentRecord,
    StudentRequestView,
    TeacherRequests,
    ApproveToStudent,
    StartQuiz,
    StudentsOfTeacher,
    generatePdf,
)

urlpatterns = [
    path("student/submit/", SubmitStudentQuiz.as_view()),
    path("student/start/", StartQuiz.as_view()),
    path("student/record/<int:fk>", StudentRecord.as_view()),
    path("teacher/record/<int:pk>", StudentsOfTeacher.as_view()),
    path("teacher/record/pdf/<int:pk>", generatePdf.as_view()),
    path("student/request/", StudentRequestView.as_view()),
    path("teacher/requests/", TeacherRequests.as_view()),
    path("teacher/request/<int:pk>/", ApproveToStudent.as_view()),
]
