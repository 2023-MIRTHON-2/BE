from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class CustomRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location', 'is_ceo']

    def create(self, request):
        is_ceo = request.pop('is_ceo')

        if is_ceo:
            user = User.objects.create_user(username=request['username'],
                                            realname=request['realname'],
                                            phone=request['phone'],
                                            license=request['license'],
                                            category=request['category'],
                                            location=request['location'],
                                            is_ceo=True)
        else:
            user = User.objects.create_user(username=request['username'],
                                            realname=request['realname'],
                                            phone=request['phone'],
                                            license='0000000000',
                                            category='아무것도 아님',
                                            location='아무것도 아님',
                                            is_ceo=False)
        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']

