from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Place, ImpossibleDate, PlaceImage
from users.models import User
import time


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['id', 'placeImage']


class PlaceListSerializer(serializers.ModelSerializer):
    placeImage = PlaceImageSerializer(read_only=True, source='placeimage_set.first')

    class Meta:
        model = Place
        fields = ['id', 'placeName', 'placeImage', 'business', 'location', 'article', 'cost']


class ImpossibleDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpossibleDate
        fields = ['id', 'impossibleDate']


class PlaceSerializer(serializers.ModelSerializer):
    placeImage_list = PlaceImageSerializer(many=True, read_only=True, source='placeimage_set')
    impossibleDate_list = ImpossibleDateSerializer(many=True, read_only=True, source='impossibledate_set')
    ceoId = ReadOnlyField(source='ceoId.id')

    class Meta:
        model = Place
        fields = ['id', 'ceoId', 'placeName', 'placeImage_list', 'licenseNum', 'lease', 'business', 'location',
                  'article', 'cost', 'impossibleDate_list']

    def create(self, validated_data):
        images_data = self.context.get('request').FILES  # 왜 noneType이지? -> context를 설정해줘야한다. 어떻게? -> view에서 serializer를 사용할 때 context를 설정해준다.
        place = Place.objects.create(**validated_data)
        for image_data in images_data.getlist('placeImage'):
            PlaceImage.objects.create(placeId=place, placeImage=image_data)
        for date_data in self.context.get('request').data.getlist('impossibleDate'):
            ImpossibleDate.objects.create(placeId=place, impossibleDate=int(date_data))
            # 예시: 1698883200

        return place
