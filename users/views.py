# from django.shortcuts import render
# from django.contrib.auth.models import User
#
# from rest_framework.response import Response
# from rest_framework import generics, status
#
# from .serializers import RegisterSerializer, LoginSerializer
#
# from django.conf import settings
# from rest_framework.decorators import api_view
# import requests
#
# API_KEY = settings.API_KEY
#
#
# class RegisterView(generics.CreateAPIView): #createAPIView(generices) 사용 구현
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#
# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data
#         return Response({"token": token.key}, status = status.HTTP_200_OK)
#
#
#


#

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from django.conf import settings
import requests

API_KEY = settings.API_KEY

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # RegisterSerializer를 사용하여 사용자 데이터 검증
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # API로 사업자 등록 번호 검증
        registration_number = serializer.validated_data['profile']['registration']
        api_url = f'https://bizno.net/api/fapi?key={API_KEY}&gb=1&q={registration_number}&type=json&pagecnt=1'

        print(api_url)

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.

            data = response.json()
            items = data.get('items', [])

            if items:
                company_data = items[0]  # 첫 번째 회사 정보를 가져옵니다.
                company_name = company_data.get('company', '')

                if company_name:
                    # 유효한 사업자 등록 번호인 경우 사용자 생성
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({'error': 'API 호출 중 오류 발생'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)
