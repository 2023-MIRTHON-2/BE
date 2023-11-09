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
    class Meta:
        model = Place
        fields = ['id', 'placeName', 'placeImage', 'business', 'location', 'article', 'cost']

    id = serializers.IntegerField(read_only=True)
    placeName = serializers.CharField()
    placeImage = PlaceImageSerializer(many=False, read_only=True, source='placeImage_set')
    business = serializers.CharField()
    location = serializers.CharField()
    article = serializers.CharField()
    cost = serializers.CharField()


class ImpossibleDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpossibleDate
        fields = ['id', 'impossibleDate']


class PlaceSerializer(serializers.ModelSerializer):
    placeImage_set = PlaceImageSerializer(many=True, read_only=True)
    impossibleDate_set = ImpossibleDateSerializer(many=True, read_only=True)
    ceoId = ReadOnlyField(source='ceoId.id')
    lease = serializers.CharField(required=False)

    class Meta:
        model = Place
        fields = ['id', 'ceoId', 'placeName', 'placeImage_set', 'licenseNum', 'lease', 'business', 'location',
                  'article', 'cost', 'impossibleDate_set']

    def create(self, validated_data):
        images_data = self.context['request'].FILES
        place = Place.objects.create(**validated_data)
        for image_data in images_data.getlist('placeImage'):
            PlaceImage.objects.create(placeId=place, placeImage=image_data)
        return place
