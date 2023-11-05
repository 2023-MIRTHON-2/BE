from django.core import serializers
from rest_framework import serializers
from .models import Place


class PlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'placeName', 'placeImageUrl', 'category', 'location', 'article', 'cost']

    Meta.model = Place
    id = serializers.IntegerField(read_only=True)
    placeName = serializers.CharField()
    placeImageUrl = serializers.CharField()
    category = serializers.CharField()
    location = serializers.CharField()
    article = serializers.CharField()
    cost = serializers.CharField()


