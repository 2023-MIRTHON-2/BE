from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Place, ImpossibleDate, PlaceImage
from users.models import User


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
    placeImage = PlaceImageSerializer(source='placeImage_set', many=False, read_only=True)
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

    class Meta:
        model = Place
        fields = ['id', 'ceoId', 'placeName', 'placeImage_set', 'licenseNum', 'lease', 'business', 'location',
                  'article', 'cost', 'impossibleDate_set']

    def create(self, validated_date):
        placeImage_set = self.context['request'].FILES.getlist('placeImage_set')
        impossibleDate_set = self.context['request'].data.getlist('impossibleDate_set')
        place = Place.objects.create(**validated_date)
        for image in placeImage_set:
            PlaceImage.objects.create(placeId=place, placeImage=image)
        for date in impossibleDate_set:
            ImpossibleDate.objects.create(placeId=place, impossibleDate=date)
        return place
