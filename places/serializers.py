import os

from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Place, ImpossibleDate, PlaceImage
from users.models import User
import base64
from baloyeogi import settings
import time


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['id', 'placeImage']

    def create(self, validated_data):
        placeImage = PlaceImage.objects.create(**validated_data)
        placeImage.save()
        return placeImage


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

    class Meta:
        model = Place
        fields = ['id', 'ceoId', 'placeName', 'placeImage_set', 'licenseNum', 'lease', 'business', 'location',
                  'article', 'cost', 'impossibleDate_set']

    def create(self, validated_data):
        place = Place.objects.create(**validated_data)

        # lease
        lease = self.context['request'].data.get('lease')
        if lease is not None:
            lease = lease.split(',')[1]
            lease = base64.b64decode(lease)
            lease_name = str(place.id) + '.pdf'
            lease_path = os.path.join(settings.MEDIA_ROOT, 'lease', lease_name)
            lease_file = open(lease_path, 'wb')
            lease_file.write(lease)
            lease_file.close()
            place.lease = 'lease/' + lease_name

        # placeImage_set
        placeImage_set = self.context['request'].data.get('placeImage_set')
        if placeImage_set is not None:
            for placeImage in placeImage_set:
                placeImage = placeImage.split(',')[1]
                placeImage = base64.b64decode(placeImage)
                placeImage_name = str(place.id) + '_' + str(time.time()) + '.jpg'
                placeImage_path = os.path.join(settings.MEDIA_ROOT, 'placeImage', placeImage_name)
                placeImage_file = open(placeImage_path, 'wb')
                placeImage_file.write(placeImage)
                placeImage_file.close()
                PlaceImage.objects.create(placeId=place, placeImage='placeImage/' + placeImage_name)

        # impossibleDate_set
        impossibleDate_set = self.context['request'].data.get('impossibleDate_set')
        if impossibleDate_set is not None:
            for impossibleDate in impossibleDate_set:
                ImpossibleDate.objects.create(placeId=place, impossibleDate=impossibleDate)

        place.save()
