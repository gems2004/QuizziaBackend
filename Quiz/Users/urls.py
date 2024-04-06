from django.urls import path, include
from .views.TeacherViews import (
    RegisterTeacher,
    RetrieveTeacher,
    GetAllTeachers,
    RenewSubscription,
)
from .views.ManagerViews import CreateManager, RetrieveManager, GetAllManagers
from .views.StudentViews import (
    RegisterStudent,
    RetrieveStudent,
    Students,
    GetAllStudents,
)
from .views.UserViews import Logout, resetpassword
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", Logout.as_view()),
    path("password-reset/", resetpassword.as_view()),
    path("teacher/register/", RegisterTeacher.as_view()),
    path("teachers/", GetAllTeachers.as_view()),
    path("teacher/<int:pk>", RetrieveTeacher.as_view()),
    path("teacher/renew/", RenewSubscription.as_view()),
    path("student/register/", RegisterStudent.as_view()),
    path("students/<int:fk>", Students.as_view()),
    path("student/<int:pk>", RetrieveStudent.as_view()),
    path("students/", GetAllStudents.as_view()),
    path("manager/create/", CreateManager.as_view()),
    path("managers/", GetAllManagers.as_view()),
    path("manager/<int:pk>", RetrieveManager.as_view()),
]
