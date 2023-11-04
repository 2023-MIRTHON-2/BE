from .models import User, Category
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    realname = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    registration = serializers.CharField(required=True)
    # document = serializers.FileField(required=True)
    category = serializers.ChoiceField(choices=[(tag.value, tag.value) for tag in Category])
    location = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'username': self.validated_data.get('username', ''),
            'realname': self.validated_data.get('realname', ''),
            'phone': self.validated_data.get('phone', ''),
            'registration': self.validated_data.get('registration', ''),
            # 'document': self.validated_data.get('document', ''),
            'category': self.validated_data.get('category', ''),
            'location': self.validated_data.get('location', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.profile.nickname = self.cleaned_data.get('nickname')
        user.profile.phone = self.cleaned_data.get('phone')
        user.profile.registration = self.cleaned_data.get('registration')
        # user.profile.document = self.cleaned_data.get('document')
        user.profile.category = self.cleaned_data.get('category')
        user.profile.location = self.cleaned_data.get('location')
        user.save()
        adapter.save_user(request, user, self)
        return user


class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'realname', 'phone', 'registration', 'category', 'location')




# from django.contrib.auth.models import User
# from django.contrib.auth.password_validation import validate_password
# from django.contrib.auth import authenticate
# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from rest_framework.validators import UniqueValidator

# from .models import User, Category  # 수정: User 모델 임포트


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         validators=[validate_password]
#     )
#     password2 = serializers.CharField(write_only=True, required=True)

#     # User 관련 필드 추가
#     nickname = serializers.CharField(source='User.nickname', required=True)
#     phone = serializers.CharField(source='User.phone', required=True)
#     registration = serializers.CharField(source='User.registration', required=True)
#     #document = serializers.FileField(required=True)
#     category = serializers.ChoiceField(source='User.category', choices=[(tag.value, tag.value) for tag in Category])
#     location = serializers.CharField(source='User.location', required=True)


#     class Meta:
#         model = User
#         fields = (
#         'username', 'password', 'password2', 'email', 'nickname', 'phone', 'registration', 'category',
#         'location')

#     def validate(self, data):
#         if data['password'] != data['password2']:
#             raise serializers.ValidationError(
#                 {"password": "비밀번호가 일치하지 않습니다."}
#             )
#         return data

#     def create(self, validated_data):
#         User_data = validated_data.pop('User')  # User 관련 데이터 추출

#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#         )
#         user.set_password(validated_data['password'])
#         user.save()

#         # User 생성, User_data는 validated_data에서 추출한 User 관련 데이터를 사용
#         User.objects.create(
#             user=user,
#             nickname=User_data['nickname'],
#             phone=User_data['phone'],
#             registration=User_data['registration'],
#             category=User_data['category'],
#             location=User_data['location']
#         )

#         # Token 생성
#         Token.objects.create(user=user)

#         return user


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True, write_only=True)

#     def validate(self, data):
#         user = authenticate(**data)
#         if user:
#             token = Token.objects.get(user=user)
#             return token
#         raise serializers.ValidationError(
#             {"error": "제공된 자격 증명으로 로그인할 수 없습니다."}
#         )
