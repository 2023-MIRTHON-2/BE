import enum
import datetime

from django.db import models


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
    presidentId = models.ForeignKey('users.User', on_delete=models.CASCADE)
    PlaceImageUrl = models.CharField(max_length=100)
    licenseNum = models.CharField(max_length=100)
    # lease = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=128, choices=Category.choices())
    location = models.TextField()
    article = models.TextField()
    cost = models.CharField(max_length=100)
    startDate = models.DateField(default=datetime.date.today)
    endDate = models.DateField(default=datetime.date.today)
    # 들어온 사업 계획서

