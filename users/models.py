import enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Category(enum.Enum):
    요식업 = '요식업'
    주점 = '주점'
    제조업 = '제조업'
    도소매 = '도소매'

    @classmethod
    def choices(cls):
        # 이 메서드는 enum의 멤버들을 (실제 값, 사람이 읽을 수 있는 이름) 형태의 튜플로 변환합니다.
        return [(key.value, key.name) for key in cls]
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=128) # 이름
    phone = models.CharField(max_length=128) # 전화번호, 수정됨
    registration = models.CharField(max_length=10) # 사업자번호, 수정됨
   # document = models.FileField(upload_to='documents/')  # 문서 파일
   #  category = models.CharField(max_length=128, choices=[(status.value, status.name) for status in Category]) # 업종
    category = models.CharField(max_length=128, choices=Category.choices())
    location = models.TextField() # 위치


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)