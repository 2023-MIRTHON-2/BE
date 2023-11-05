from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from .models import User, Category
from rest_framework import serializers

from .serializers import get_register_serializer

from .serializers import CustomRegisterSerializer, CustomRenterRegisterSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

API_KEY = settings.API_KEY


class CheckLicenseView(APIView):

    # 사업자 등록번호 유효한지 확인
    def get(self, request, license_number):
        api_url = f'https://bizno.net/api/fapi?key={API_KEY}&gb=1&q={license_number}&type=json&pagecnt=1'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
            data = response.json()
            items = data.get('items', [])
            if items:
                company_data = items[0]  # 첫 번째 회사 정보를 가져옵니다.
                company_name = company_data.get('company', '')
                if company_name:  # 유효한 사업자 등록 번호인 경우
                    return Response({'message': f'{company_name}: 유효한 사업자 등록 번호입니다.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({'error': 'API 호출 중 오류 발생'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class CustomRegisterView(APIView):
#     def get_serializer_class(self):
#         # URL에서 "registration_type" 파라미터를 가져옵니다.
#         registration_type = self.request.query_params.get('registration_type')
#
#         # "registration_type"이 "renter"인 경우 Renter에 필요한 필드를 사용하는 시리얼라이저를 반환합니다.
#         if registration_type == "renter":
#             return CustomRenterRegisterSerializer
#
#         # 기본적으로는 CEO에 필요한 필드를 사용하는 시리얼라이저를 반환합니다.
#         return CustomRegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer_class = self.get_serializer_class()
#         serializer = serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'message': 'Registration successful', 'user_id': user.id})
#         return Response(serializer.errors, status=400)

    def registration_view(request, registration_type):
        # registration_type에 따른 직렬라이저를 얻습니다.
        serializer_class = get_register_serializer(registration_type)

        if serializer_class is None:
            return Response({'error': 'Invalid registration type'}, status=400)

        if request.method == 'POST':
            # 직렬라이저를 사용하여 요청 데이터를 처리합니다.
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({'message': 'Registration successful', 'user_id': user.id})
            else:
                return Response(serializer.errors, status=400)

        return Response({'error': 'Unsupported HTTP method'}, status=400)