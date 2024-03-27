from rest_framework.permissions import BasePermission
from Users.models import Student
from StudentDoQuiz.models import StudentRequest


class TeacherPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "Teacher")


class StudentPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "Student")


class TeacherApprovedToStudent(BasePermission):
    def has_permission(self, request, view):
        try:
            student = Student.objects.get(user=request.user)
            student_request = (
                StudentRequest.objects.filter(student=student)
                .order_by("-created_at")
                .first()
            )
        except Exception as e:
            return e
        if student_request.approved == None:
            return False
        if request.user.role == "Student" and student_request.approved == True:
            return True
