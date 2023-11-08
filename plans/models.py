from django.db import models
from users.models import User
from places.models import Place
import enum
import datetime


class Category(enum.Enum):
    요식업 = '요식업'
    주점 = '주점'
    제조업 = '제조업'
    도소매 = '도소매'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Plan(models.Model):
    ceoId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ceos")  #사업자
    renterId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="renters") #대여자
    placeId = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="places") #사업장
    name = models.CharField(max_length=128) #사업 계획서 작성하는 이용자가 넣는 이름
    phone = models.CharField(max_length=128) #사업 계획서 작성하는 이용자가 넣는 폰번호
    startDate = models.DateField(default=datetime.date.today) #계약(희망) 시작 날짜
    endDate = models.DateField(default=datetime.date.today) #계약(희망) 종료 날짜
    category = models.CharField(max_length=128, choices=Category.choices()) #업종
    information = models.TextField() #사업정보
    inquiry = models.TextField() #문의사항
    received_date = models.DateTimeField(auto_now_add=True) #접수 일자
    approval = models.BooleanField(default=False) #계약 승인 여부
