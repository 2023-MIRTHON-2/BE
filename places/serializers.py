from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Place
from users.models import User


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'placeName', 'placeImageUrl', 'business', 'location', 'article', 'cost']

    Meta.model = Place
    id = serializers.IntegerField(read_only=True)
    placeName = serializers.CharField()
    placeImageUrl = serializers.CharField()
    business = serializers.CharField()
    location = serializers.CharField()
    article = serializers.CharField()
    cost = serializers.CharField()


class PlaceDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id']
    Meta.model = Place
    id = serializers.IntegerField(read_only=True)


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['placeImage']
    Meta.model = Place
    placeImage = serializers.CharField()


class PlaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'placeName', 'placeImageList', 'business', 'location', 'article', 'cost', 'startDate',
                  'endDate']
    Meta.model = Place
    id = serializers.IntegerField(read_only=True)
    placeName = serializers.CharField()
    placeImageList = PlaceImageSerializer(many=True, read_only=True, source='placeimage_set')
    business = serializers.CharField()
    location = serializers.CharField()
    article = serializers.CharField()
    cost = serializers.CharField()
    startDate = serializers.DateField()
    endDate = serializers.DateField()

