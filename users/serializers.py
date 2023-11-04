from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class CustomRegisterSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']

    username = serializers.CharField(required=True)
    realname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    license = serializers.CharField(required=True)
    # document = serializers.FileField(required=True)
    category = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in Category])
    location = serializers.CharField(required=True)

    def create(self, request):
        user = User(username=request.data['username'],
                    realname=request.data['realname'],
                    phone=request.data['phone'],
                    license=request.data['license'],
                    category=request.data['category'],
                    location=request.data['location'],
                    )
        user.set_password(request.data['password'])
        user.save()
        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']
