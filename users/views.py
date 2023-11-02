from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView): #createAPIView(generices) 사용 구현
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


