from .models import User, Category
from rest_framework import serializers
import base64

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter

class CustomRegisterSerializer(RegisterSerializer):
    id = serializers.IntegerField(read_only=True)
    realname = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=50)
    is_ceo = serializers.BooleanField(default=True)

    def get_cleaned_data(self):
        # super 클래스의 get_cleaned_data 메소드를 호출하여 기본 데이터를 가져옵니다.
        data = super().get_cleaned_data()
        # 추가 필드를 cleaned_data에 추가합니다.
        data['realname'] = self.validated_data.get('realname', '')
        data['phone'] = self.validated_data.get('phone', '')
        data['is_ceo'] = self.validated_data.get('is_ceo', True)
        return data

    def save(self, request):
        # 부모 클래스의 save 메소드를 호출하여 사용자를 생성합니다.
        user = super().save(request)
        # 추가 필드를 사용자 인스턴스에 저장합니다.
        user.realname = self.validated_data.get('realname', '')
        user.phone = self.validated_data.get('phone', '')
        user.is_ceo = self.validated_data.get('is_ceo', True)
        user.save()
        return user
class CustomRenterRegisterSerializer(RegisterSerializer):
    id = serializers.IntegerField(read_only=True)
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
        fields = ['id','username', 'realname', 'phone', 'is_ceo']

