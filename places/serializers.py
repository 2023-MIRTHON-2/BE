from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Place, ImpossibleDate, PlaceImage
from users.models import User
import time


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['placeImageUrl']


class PlaceListSerializer(serializers.ModelSerializer):
    # placeImageUrl = PlaceImageSerializer(read_only=True, source='placeimage_set.first') # object로 보내지 않고, 하나만 보낸다.
    placeImageUrl = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'placeName', 'placeImageUrl', 'business', 'location', 'article', 'cost']

    def get_placeImageUrl(self, obj):
        placeImage = PlaceImage.objects.filter(placeId=obj).first()
        if placeImage is None:
            return None
        return placeImage.placeImageUrl


class ImpossibleDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpossibleDate
        fields = ['id', 'impossibleDate']


class PlaceSerializer(serializers.ModelSerializer):
    placeImageUrl = PlaceImageSerializer(many=True, read_only=True, source='placeimage_set')
    impossibleDate_list = ImpossibleDateSerializer(many=True, read_only=True, source='impossibledate_set')
    ceoId = ReadOnlyField(source='ceoId.id')

    class Meta:
        model = Place
        fields = ['id', 'ceoId', 'placeName', 'placeImageUrl', 'licenseNum', 'lease', 'business', 'location',
                  'article', 'cost', 'impossibleDate_list']

    def create(self, validated_data):
        images_data = self.context.get('request').FILES
        place = Place.objects.create(**validated_data)
        for image_data in images_data.getlist('placeImageUrl'):
            PlaceImage.objects.create(placeId=place, placeImageUrl=image_data)
        for date_data in self.context.get('request').data.getlist('impossibleDate'):
            ImpossibleDate.objects.create(placeId=place, impossibleDate=int(date_data))

        return place
