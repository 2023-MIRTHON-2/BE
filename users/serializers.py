from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class CustomRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location', 'is_ceo']

    def create(self, request):
        is_ceo = request.data.get('is_ceo', True)

        if is_ceo:
            user = User.objects.create_user(
                        **request
                        )

        else:
            user = User.objects.create_user(
                        **request
                        )


        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']

