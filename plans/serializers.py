from rest_framework import serializers
from .models import Plan


# class ImpossibleDateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImpossibleDate
#         fields = ['impossibleDate']


class PlanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    ceoId = serializers.CharField(source='ceoId.username', read_only=True)
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'ceoId', 'renterId', 'placeId', 'name', 'phone', 'startDate', 'endDate', 'business',
                  'information', 'inquiry', 'received_date', 'approval']


class PlanShowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'phone', 'startDate', 'endDate', 'business', 'information', 'inquiry']


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
    ceoBusiness = serializers.SerializerMethodField()
    ceoLocation = serializers.SerializerMethodField()
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    renterPhone = serializers.SerializerMethodField()
    renterBusiness = serializers.SerializerMethodField()
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)
    placeStartDate = serializers.SerializerMethodField()
    placeEndDate = serializers.SerializerMethodField()
    placeCost = serializers.SerializerMethodField()

    def get_ceoPhone(self, obj):
        return obj.ceoId.phone if obj.ceoId else None

    def get_ceoBusiness(self, obj):
        return obj.placeId.business if obj.placeId else None

    def get_ceoLocation(self, obj):
        return obj.placeId.location if obj.placeId else None

    def get_renterPhone(self, obj):
        return obj.renterId.phone if obj.renterId else None

    def get_renterBusiness(self, obj):
        return obj.business if obj.renterId else None

    def get_placeStartDate(self, obj):
        return obj.placeId.startDate if obj.placeId else None

    def get_placeEndDate(self, obj):
        return obj.placeId.endDate if obj.placeId else None

    def get_placeCost(self, obj):
        return obj.placeId.cost if obj.placeId else None

    class Meta:
        model = Plan  # 실제 모델 이름으로 교체해야 합니다.
        fields = [
            'id', 'ceoId', 'ceoPhone', 'ceoBusiness', 'ceoLocation', 'renterId', 'renterPhone', 'renterBusiness',
            'placeId', 'placeStartDate', 'placeEndDate', 'placeCost'
        ]
        read_only_fields = ('id', 'ceoId', 'renterId', 'placeId')



class ApprovalContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = [
            'id', 'renterId',
            'placeId', 'startDate', 'endDate'
        ]
        read_only_fields = ('id', 'renterId', 'placeId')
