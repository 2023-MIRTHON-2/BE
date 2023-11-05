from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
class CustomRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location', 'is_ceo']

    def create(self, request):
        user = User.objects.create_user(username=request['username'],
                                        realname=request['realname'],
                                        phone=request['phone'],
                                        license=request['license'],
                                        category=request['category'],
                                        location=request['location'],
                                        is_ceo=True)

        return user

class CustomRenterRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone']

    def create(self, request):
        user = User.objects.create_user(username=request['username'],
                                        realname=request['realname'],
                                        phone=request['phone'],
                                        # license=request['license'],
                                        # category=request['category'],
                                        # location=request['location'],
                                        is_ceo=False)

        return user

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']

