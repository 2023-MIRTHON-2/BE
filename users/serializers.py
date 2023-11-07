from .models import User, Category
from rest_framework import serializers
import base64

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter

class CustomRegisterSerializer(RegisterSerializer):
    # 기존 필드 정의
    realname = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=50)
    license = serializers.CharField(max_length=50)
    document = serializers.CharField()  # document는 base64 인코딩된 문자열을 받음
    category = serializers.CharField(max_length=128)
    location = serializers.CharField(max_length=255)
    is_ceo = serializers.BooleanField(default=True)

    def validate_document(self, value):
        # document 필드의 base64 데이터를 검증하고 디코딩합니다.
        try:
            # base64로 인코딩된 문자열을 확인합니다.
            return base64.b64decode(value)  # 디코딩된 데이터를 반환합니다.
        except TypeError:
            raise serializers.ValidationError("이 문서 필드는 유효한 base64 인코딩 문자열이어야 합니다.")
        # 문서 데이터가 유효하지 않으면 예외가 발생합니다.

    def get_cleaned_data(self):
        # super 클래스의 get_cleaned_data 메소드를 호출하여 기본 데이터를 가져옵니다.
        data = super().get_cleaned_data()
        # 추가 필드를 cleaned_data에 추가합니다.
        data['realname'] = self.validated_data.get('realname', '')
        data['phone'] = self.validated_data.get('phone', '')
        data['license'] = self.validated_data.get('license', '')
        data['document'] = self.validated_data.get('document', '')
        data['category'] = self.validated_data.get('category', '')
        data['location'] = self.validated_data.get('location', '')
        data['is_ceo'] = self.validated_data.get('is_ceo', True)
        return data

    def save(self, request):
        # 부모 클래스의 save 메소드를 호출하여 사용자를 생성합니다.
        user = super().save(request)
        # 추가 필드를 사용자 인스턴스에 저장합니다.
        user.realname = self.validated_data.get('realname', '')
        user.phone = self.validated_data.get('phone', '')
        user.license = self.validated_data.get('license', '')
        user.category = self.validated_data.get('category', '')
        user.document = self.validated_data.get('document', '')
        user.location = self.validated_data.get('location', '')
        user.is_ceo = self.validated_data.get('is_ceo', True)
        user.save()
        return user
class CustomRenterRegisterSerializer(RegisterSerializer):
    realname = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=50)
    is_ceo = serializers.BooleanField(default=False)

    def get_cleaned_data(self):
        # super 클래스의 get_cleaned_data 메소드를 호출하여 기본 데이터를 가져옵니다.
        data = super().get_cleaned_data()
        # 추가 필드를 cleaned_data에 추가합니다.
        data['realname'] = self.validated_data.get('realname', '')
        data['phone'] = self.validated_data.get('phone', '')
        data['is_ceo'] = self.validated_data.get('is_ceo', False)
        return data

    def save(self, request):
        # 부모 클래스의 save 메소드를 호출하여 사용자를 생성합니다.
        user = super().save(request)
        # 추가 필드를 사용자 인스턴스에 저장합니다.
        user.realname = self.validated_data.get('realname', '')
        user.phone = self.validated_data.get('phone', '')
        user.is_ceo = self.validated_data.get('is_ceo', False)
        user.save()
        return user

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']

