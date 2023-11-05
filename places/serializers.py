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
