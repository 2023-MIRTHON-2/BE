from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    ceoId = serializers.CharField(source='ceoId.username', read_only=True)
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'ceoId', 'renterId', 'placeId', 'name', 'phone', 'startDate', 'endDate', 'bussiness', 'information', 'inquiry',
                  'received_date', 'approval']


class PlanShowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Plan
        fields = ['id', 'name', 'phone', 'startDate', 'endDate', 'bussiness', 'information', 'inquiry']


class PlanRenterShowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)
    received_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'placeId', 'startDate', 'endDate', 'received_date', 'approval']


class PlanCeoShowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    received_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'renterId', 'placeId', 'startDate', 'endDate', 'received_date']


class ContractShowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    ceoId = serializers.CharField(source='ceoId.username', read_only=True)
    ceoPhone = serializers.SerializerMethodField()
    ceoBussiness = serializers.SerializerMethodField()
    ceoLocation = serializers.SerializerMethodField()
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    renterPhone = serializers.SerializerMethodField()
    renterBussiness = serializers.SerializerMethodField()
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)
    placeStartDate = serializers.SerializerMethodField()
    placeEndDate = serializers.SerializerMethodField()
    placeCost = serializers.SerializerMethodField()

    def get_ceoPhone(self, obj):
        return obj.ceoId.phone if obj.ceoId else None

    def get_ceoBussiness(self, obj):
        return obj.placeId.bussiness if obj.placeId else None

    def get_ceoLocation(self, obj):
        return obj.placeId.location if obj.placeId else None

    def get_renterPhone(self, obj):
        return obj.renterId.phone if obj.renterId else None

    def get_renterBussiness(self, obj):
        return obj.bussiness if obj.renterId else None

    def get_placeStartDate(self, obj):
        return obj.placeId.startDate if obj.placeId else None

    def get_placeEndDate(self, obj):
        return obj.placeId.endDate if obj.placeId else None

    def get_placeCost(self, obj):
        return obj.placeId.cost if obj.placeId else None

    class Meta:
        model = Plan  # 실제 모델 이름으로 교체해야 합니다.
        fields = [
            'id', 'ceoId', 'ceoPhone', 'ceoBussiness', 'ceoLocation',
            'renterId', 'renterPhone', 'renterBussiness',
            'placeId', 'placeStartDate', 'placeEndDate', 'placeCost'
        ]
        read_only_fields = ('id', 'ceoId', 'renterId', 'placeId')