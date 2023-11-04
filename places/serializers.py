from django.core import serializers
from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    presidentId = serializers.CharField(source='presidentId.username', read_only=True)
    class Meta:
        model = Place
        fields = ['id', 'presidentId', 'placeName', 'placeImageUrl', 'licenseNum', 'category', 'location', 'article',
                  'cost', 'startDate', 'endDate', 'about']
