from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    ceoId = serializers.CharField(source='ceoId.username', read_only=True)
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)

    class Meta:
        model = Plan
        fields = ['ceoId', 'renterId', 'placeId', 'name', 'phone', 'startDate', 'endDate', 'category', 'information', 'inquiry',
                  'received_date', 'approval']


class PlanShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['name', 'phone', 'startDate', 'endDate', 'category', 'information', 'inquiry']


class PlanRenterShowSerializer(serializers.ModelSerializer):
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)
    received_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Plan
        fields = ['placeId', 'startDate', 'endDate', 'received_date', 'approval']


class PlanCeoShowSerializer(serializers.ModelSerializer):
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    received_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Plan
        fields = ['renterId', 'placeId', 'startDate', 'endDate', 'received_date']
