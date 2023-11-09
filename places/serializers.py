from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Place
from users.models import User


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'presidentId', 'placeName', 'placeImageUrl', 'bussiness', 'location', 'article', 'cost']

    Meta.model = Place
    id = serializers.IntegerField(read_only=True)
    placeName = serializers.CharField()
    placeImageUrl = serializers.CharField()
    bussiness = serializers.CharField()
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
        fields = ['id', 'placeImage']

    Meta.model = Place
    id = serializers.IntegerField(read_only=True)
    placeImage = serializers.ImageField()


class PlaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'presidentId', 'placeName', 'placeImageUrl', 'licenseNum', 'lease', 'business', 'location',
                  'article', 'cost', 'startDate', 'endDate', 'placeImage']

    Meta.model = Place
    id = serializers.IntegerField(read_only=True)
    presidentId = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    placeName = serializers.CharField()
    placeImageUrl = serializers.CharField()
    licenseNum = serializers.CharField()
    lease = serializers.FileField()
    business = serializers.CharField()
    location = serializers.CharField()
    article = serializers.CharField()
    cost = serializers.CharField()
    startDate = serializers.DateTimeField()
    endDate = serializers.DateTimeField()
    placeImage = PlaceImageSerializer(many=True, read_only=True)
