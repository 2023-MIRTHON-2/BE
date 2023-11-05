from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class CustomRenterRegisterSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone']

    username = serializers.CharField(required=True)
    realname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    #
    # license = serializers.CharField(read_only=True)
    # category = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in Category], read_only=True)
    # location = serializers.CharField(read_only=True)
    def create(self, request):
        user = User(username=request.data['username'],
                    realname=request.data['realname'],
                    phone=request.data['phone'],
                    )
        user.set_password(request.data['password'])
        user.save()
        print(user)
        return user


class CustomRenterUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone']


class CustomRegisterSerializer(RegisterSerializer):

    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']

    username = serializers.CharField(required=True)
    realname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    license = serializers.CharField(required=True)
    category = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in Category], required=True)
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



def get_register_serializer(registration_type):
    if registration_type == 'ceo':
        return CustomRegisterSerializer
    elif registration_type == 'renter':
        return CustomRenterRegisterSerializer
    else:
        return None