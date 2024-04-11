from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import Response, status

from Users.permissions import TeacherPermissions
from Users.serializers.UserSerializers import ResetPasswordSerializer


class Logout(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "logged out"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


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
