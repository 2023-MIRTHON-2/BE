from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
class CustomRegisterSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location', 'is_ceo']

    username = serializers.CharField(required=True)
    realname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    license = serializers.CharField(required=False)
    category = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in Category], required=False)
    location = serializers.CharField(required=False)
    is_ceo = serializers.BooleanField()

    def create(self, request):
        is_ceo = request.data.get('is_ceo', True)

        if is_ceo:
            user = User.objects.create_user(
                        **request
                        )

        else:
            user = User.objects.create_user(
                        username=request.data['username'],
                        realname=request.data['realname'],
                        phone=request.data['phone'],
                        is_ceo=request.data['is_ceo']
                        )


        # user.set_password(request.data['password'])
        # user.save()
        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'realname', 'phone', 'license', 'category', 'location']

