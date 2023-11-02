from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

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

