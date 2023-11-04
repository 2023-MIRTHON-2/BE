from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    realname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    license = serializers.CharField(required=True)
    # document = serializers.FileField(required=True)
    category = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in Category])
    location = serializers.CharField(required=True)

    def get_cleaned_data(self):  # 사용자가 입력한 데이터를 가져옵니다.
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'username': self.validated_data.get('username', ''),
            'realname': self.validated_data.get('realname', ''),
            'phone': self.validated_data.get('phone', ''),
            'license': self.validated_data.get('license', ''),
            # 'document': self.validated_data.get('document', ''),
            'category': self.validated_data.get('category', ''),
            'location': self.validated_data.get('location', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.nickname = self.cleaned_data.get('nickname')
        user.phone = self.cleaned_data.get('phone')
        user.license = self.cleaned_data.get('license')
        # user.profile.document = self.cleaned_data.get('document')
        user.category = self.cleaned_data.get('category')
        user.location = self.cleaned_data.get('location')
        user.save()
        adapter.save_user(request, user, self)
        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'realname', 'phone', 'license', 'category', 'location')
