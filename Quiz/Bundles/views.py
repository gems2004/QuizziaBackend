from django.shortcuts import render
from .serializer import BundleSerializer
from .models import Bundle
from rest_framework.views import APIView, Response, status
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from Users.permissions import TeacherPermissions


# Create your views here.
class BundleView(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated,  TeacherPermissions | IsAdminUser]

    def get(self, request):
        try:
            bundles = Bundle.objects.all()
            serializer = BundleSerializer(bundles, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({'err': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = BundleSerializer(data=request.data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'err': str(e)}, status.HTTP_400_BAD_REQUEST)


class SpecificBundle(APIView):
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated, TeacherPermissions | IsAdminUser]

    def get(self, request, pk):
        try:
            bundle = Bundle.objects.get(pk=pk)
            serializer = BundleSerializer(bundle)
        except Exception as e:
            return Response({'err': str(e)}, status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
            bundle = Bundle.objects.get(pk=pk)
            serializer = BundleSerializer(bundle, data=request.data, many=False)
        except Exception as e:
            return Response({'err': str(e)})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            bundle = Bundle.objects.get(pk=pk)
            bundle.delete()
            return Response('bundle successfully deleted', status.HTTP_200_OK)
        except Exception as e:
            return Response({'err': str(e)}, status.HTTP_404_NOT_FOUND)
