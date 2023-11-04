from django.core import serializers
from rest_framework import serializers
from .models import Place


class DetailPlaceSerializer(serializers.ModelSerializer):
    presidentId = serializers.CharField(source='presidentId.username', read_only=True)
    class Meta:
        model = Place
        fields = ['id', 'presidentId', 'placeName', 'placeImageUrl', 'licenseNum', 'category', 'location', 'article',
                  'cost', 'startDate', 'endDate', 'about']


# 메인페이지용 공간 정보 리스트 조회(location, category, placeName, placeImageUrl. cost)
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['location', 'category', 'placeName', 'placeImageUrl', 'cost']

