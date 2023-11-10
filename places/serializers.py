from django.core import serializers
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Place, ImpossibleDate, PlaceImage
from utils import check_license_number


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = ['placeImageUrl']


class PlaceListSerializer(serializers.ModelSerializer):
    # placeImageUrl = PlaceImageSerializer(read_only=True, source='placeimage_set.first') # object로 보내지 않고, 하나만 보낸다.
    placeImageUrl = serializers.SerializerMethodField('get_placeImageUrl')

    def get_placeImageUrl(self, obj):
        return obj.placeimage_set.first().placeImageUrl.url

    class Meta:
        model = Place
        fields = ['id', 'placeName', 'placeImageUrl', 'business', 'location',
                  'article', 'cost']


class ImpossibleDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpossibleDate
        fields = ['impossibleDate']


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
        license_number = self.initial_data.get('licenseNum', '')
        company_number = check_license_number(license_number)
        if company_number:
            place.licenseNum = company_number  # 검증된 사업자 등록번호 저장
            place.save()  # 변경사항을 저장합니다.
        else:
            raise serializers.ValidationError("유효하지 않은 사업자 등록 번호입니다.")

        return place


class PlaceForMyPageSerializer(serializers.ModelSerializer):
    placeImageUrl = serializers.SerializerMethodField('get_placeImageUrl')

    def get_placeImageUrl(self, obj):
        return obj.placeimage_set.first().placeImageUrl.url

    class Meta:
        model = Place
        fields = ['id', 'placeName', 'licenseNum', 'placeImageUrl', 'business', 'location',
                  'article', 'cost']
