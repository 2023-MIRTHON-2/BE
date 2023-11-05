import enum
import datetime

from django.db import models
from users.models import User


class Category(enum.Enum):
    요식업 = '요식업'
    주점 = '주점'
    제조업 = '제조업'
    도소매 = '도소매'

    @classmethod
    def choices(cls):
        # 이 메서드는 enum의 멤버들을 (실제 값, 사람이 읽을 수 있는 이름) 형태의 튜플로 변환합니다.
        return [(key.value, key.name) for key in cls]


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    presidentId = models.ForeignKey(User, on_delete=models.CASCADE)
    placeName = models.CharField(max_length=100)
    placeImageUrl = models.CharField(max_length=100)
    licenseNum = models.CharField(max_length=100)
    # lease = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=128, choices=Category.choices())
    location = models.CharField(max_length=100)
    article = models.TextField() # 사업에 대한 설명
    cost = models.CharField(max_length=100)
    startDate = models.DateField(default=datetime.date.today)
    endDate = models.DateField(default=datetime.date.today)
    # 들어온 사업 계획서

    def __str__(self):
        return self.placeName

