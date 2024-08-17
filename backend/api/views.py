from django.shortcuts import render
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializer import (
     UserLoginSerializer,
     UserRegisterSerializer,
)

def TokenGeneratorView(user):
    UserRefreshToken = RefreshToken.for_user(user)
    return Response({"user_refresh_token":UserRefreshToken,"user_access_token":UserRefreshToken.access_token})


class UserRegisterView(APIView):
    
    def post(self,request):
        ClientResponse = UserRegisterSerializer(data=request.data)
        if ClientResponse.is_valid():
            password = ClientResponse.validated_data["password"]
            password1 = request.data.get("email")

            if password != password1:
               return  Response({"error":"Passwords mismatched!"},status = status.HTTP_400_BAD_REQUEST)
            
            user = ClientResponse.save()
            user.set_password(user.password)
            return Response({"success":"Wait as you are redirected to the login page"},status=status.HTTP_201_CREATED)
        return Response(ClientResponse.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request):
        ClientResponse = UserLoginSerializer(data=request.data)
        if ClientResponse.is_valid():
            username = ClientResponse.validated_data["username"]
            password = ClientResponse.validated_data["password"]

            user = authenticate(username=username,password=password)
            if user is not None:

                UserTokens = TokenGeneratorView(user)
                return Response({"access":UserTokens.user_access_token,"refresh":UserTokens.user_refresh_token},status=status.HTTP_201_CREATED)
            return Response({"error":"User not found!"},status=status.HTTP_400_BAD_REQUEST)
        return Response(ClientResponse.errors,status=status.HTTP_400_BAD_REQUEST)


