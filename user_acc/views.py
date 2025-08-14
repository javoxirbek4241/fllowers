from django.shortcuts import render
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializers, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

class RegisterApi(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':status.HTTP_200_OK, 'data':serializer.data})
        return Response({'status':status.HTTP_400_BAD_REQUEST})



class LoginApi(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user = user)
            return Response({'Token':token.key, 'status':status.HTTP_200_OK})
        return Response({'status':status.HTTP_400_BAD_REQUEST, 'error':'username yoki parol xato'})


class LogoutApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message':'Chiqildi', 'status':status.HTTP_200_OK})


class ProfileApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,  request):
        serializer = ProfileSerializer(request.user)
        return Response({'status':status.HTTP_200_OK, 'data':serializer.data})

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profil yangilandi', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
























