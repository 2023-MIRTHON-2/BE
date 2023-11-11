from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import CustomRegisterSerializer, CustomRenterRegisterSerializer, MypageCustomUserDetailSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
import requests

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
                company_number = company_data.get('bno', '')
                if company_name:  # 유효한 사업자 등록 번호인 경우
                    return Response({'message': f'{company_name}({company_number}): 유효한 사업자 등록 번호입니다.'},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({'error': 'API 호출 중 오류 발생'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterAPIView(APIView):
    def post(self, request, is_ceo):
        # Determine which serializer to use based on 'is_ceo' parameter
        if is_ceo.lower() == 'true':
            serializer = CustomRegisterSerializer(data=request.data)
        else:
            serializer = CustomRenterRegisterSerializer(data=request.data)

        # Validate the data using the serializer
        if serializer.is_valid():
            # If validation passes, save the user and generate tokens
            user = serializer.save(request=request)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            user_data = serializer.data
            user_data['id'] = user.id

            # Prepare the response
            res = Response(
                {
                    "user": user_data,
                    "message": "register success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )

            # Set the tokens in cookies
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res

        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckUsernameAPIView(APIView):
    # 사용자 이름 중복 확인
    def get(self, request, username):
        if User.objects.filter(username=username).exists():
            return Response({'message': '이미 존재하는 이름입니다.', 'available': 0}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '사용 가능한 사용자 이름입니다.', 'available': 1}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = MypageCustomUserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)