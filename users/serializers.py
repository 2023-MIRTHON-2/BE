from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer): #회원가입 시리얼라이저
    email = serializers.EmailField(
        required = True,
        validators=[UniqueValidator(queryset=User.objects.all())], #이메일에 대한 중복 검증
    )
    password = serializers.CharField( #비밀번호 검증
        write_only=True,
        required = True,
        validators = [validate_password],
    )
    password2 = serializers.CharField(write_only=True, required =True)

    class Meta:
        model = User
        fields = ('username','password','password2','email')

    def validate(self, data): #추가적으로 비밀번호 일치 여부를 확인
        if data ['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password" : "패스워드 안맞음"}
            )
        return data

    def create(self, validated_data): #create 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게함
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only = True)
#write_only 옵션을 통해 클라이언트 -> 서버 방향의 역질혈화는 가능, 서버-> 클라이언트 방향의 직렬화는 불가능

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) #토큰에서 유저 찾아 응답
            return token
        raise serializers.ValidationError(
            {"error": "제공된 자격 증명으로 로그인할 수 없습니다"}
        )