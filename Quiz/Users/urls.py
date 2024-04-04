from django.urls import path, include
from .views import (
    RegisterTeacher,
    Logout,
    RegisterStudent,
    RetrieveTeacher,
    RetrieveStudent,
    resetpassword,
    Students,
    GetAllTeachers,
    GetAllStudents,
    RenewSubscription,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("teacher/register/", RegisterTeacher.as_view()),
    path("logout/", Logout.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("student/register/", RegisterStudent.as_view()),
    path("students/<int:fk>", Students.as_view()),
    path("teacher/<int:pk>", RetrieveTeacher.as_view()),
    path("student/<int:pk>", RetrieveStudent.as_view()),
    path("password-reset/", resetpassword.as_view()),
    path("teachers/", GetAllTeachers.as_view()),
    path("students/", GetAllStudents.as_view()),
    path("teacher/renew/", RenewSubscription.as_view()),
]
