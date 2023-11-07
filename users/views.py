from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.conf import settings
import requests
from .serializers import CustomRegisterSerializer, CustomRenterRegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
import base64
from django.core.files.base import ContentFile
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
    def post(self, request, is_ceo):
        # 클라이언트로부터 전송받은 base64 인코딩된 문서 데이터
        base64_encoded_document = request.data.get('document')

        # document 필드가 있는지 확인하고 base64 데이터를 디코딩합니다.
        if base64_encoded_document:
            # base64 데이터를 디코딩하여 바이너리 데이터로 변환
            document_data = base64.b64decode(base64_encoded_document)
            request.data['document'] = document_data

        if is_ceo.lower() == 'true':
            serializer = CustomRegisterSerializer(data=request.data)
        else:
            serializer = CustomRenterRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(request=request)
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
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckUsernameAPIView(APIView):
    # 사용자 이름 중복 확인
    def get(self, request, username):
        if User.objects.filter(username=username).exists():
            return Response({'error': '이미 존재하는 사용자 이름입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': '사용 가능한 사용자 이름입니다.', 'available': 1}, status=status.HTTP_200_OK)




