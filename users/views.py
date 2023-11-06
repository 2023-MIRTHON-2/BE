from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from .serializers import CustomRegisterSerializer, CustomRenterRegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class RegisterAPIView(APIView):
    def post(self, request,is_ceo):
        # serializer = CustomRegisterSerializer(data=request.data)  # 시리얼아리저 사용해서 유저 저장

        if is_ceo.lower() == 'true':
            serializer = CustomRegisterSerializer(data=request.data)  # is_ceo가 True인 경우
        else:
            serializer = CustomRenterRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(request=request)                    # 저장
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )
            # jwt 토큰을 받아서 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)   # httponly=True : JavaScript로 쿠키를 조회할 수 없게 함
            res.set_cookie("refresh", refresh_token, httponly=True)     # XSS로부터 안전해지지만, CSRF로부터 취약해짐 => CSRF 토큰을 같이 사용해야 함
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







