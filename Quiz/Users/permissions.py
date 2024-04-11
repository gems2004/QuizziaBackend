from rest_framework.permissions import BasePermission
from Users.models import Student, Teacher
from StudentDoQuiz.models import StudentRequest
from datetime import timedelta, timezone


class TeacherPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "Teacher")


class StudentPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "Student")


class TeacherApprovedToStudent(BasePermission):
    def has_permission(self, request, view):
        try:
            curr_time = timezone.now()
            target_time = curr_time - timedelta(minutes=30)
            student = Student.objects.get(user=request.user)
            student_request = (
                StudentRequest.objects.filter(student=student)
                .filter(created_at__gte=target_time)
                .order_by("-created_at")
            )
        except Exception as e:
            return e
        if student_request.approved == None:
            return False
        if request.user.role == "Student" and student_request.approved == True:
            return True


class ManagerPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "Manager")
