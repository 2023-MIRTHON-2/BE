from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import Profile, Category  # 수정: Profile 모델 임포트


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    # Profile 관련 필드 추가
    nickname = serializers.CharField(source='profile.nickname', required=True)
    phone = serializers.CharField(source='profile.phone', required=True)
    registration =  serializers.CharField(source='profile.registration', required=True)
    #document = serializers.FileField(required=True)
    category = serializers.ChoiceField(source='profile.category', choices=[(tag.value, tag.value) for tag in Category])
    location = serializers.CharField(source='profile.location', required=True)


    class Meta:
        model = User
        fields = (
        'username', 'password', 'password2', 'email', 'nickname', 'phone', 'registration', 'category',
        'location')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')  # profile 관련 데이터 추출

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Profile 생성, profile_data는 validated_data에서 추출한 profile 관련 데이터를 사용
        Profile.objects.create(
            user=user,
            nickname=profile_data['nickname'],
            phone=profile_data['phone'],
            registration=profile_data['registration'],
            category=profile_data['category'],
            location=profile_data['location']
        )

        # Token 생성
        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "제공된 자격 증명으로 로그인할 수 없습니다."}
        )
