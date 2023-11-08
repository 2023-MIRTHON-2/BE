import enum

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Category(enum.Enum):
    요식업 = '요식업'
    주점 = '주점'
    제조업 = '제조업'
    도소매 = '도소매'

    @classmethod
    def choices(cls):
        # 이 메서드는 enum의 멤버들을 (실제 값, 사람이 읽을 수 있는 이름) 형태의 튜플로 변환합니다.
        return [(key.value, key.name) for key in cls]


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        주어진 이메일, 비밀번호 등 개인정보로 인스턴스 생성
        """

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        superuser = self.create_user(password=password)

        # superuser.is_staff = True
        # superuser.is_superuser = True
        # superuser.is_active = True

        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=True)  # 아이디
    realname = models.CharField(max_length=128)  # 실명
    phone = models.CharField(max_length=128)  # 전화번호
    is_ceo = models.BooleanField(default=False)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()

    email = None
    email_verified = None

    # class Meta:
    #     db_table = 'users'

    def __str__(self):
        return self.username