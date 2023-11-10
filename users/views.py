from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import CustomRegisterSerializer, CustomRenterRegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


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

            # Prepare the response
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
