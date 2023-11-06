from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    ceoId = serializers.CharField(source='ceoId.username', read_only=True)
    renterId = serializers.CharField(source='renterId.username', read_only=True)
    placeId = serializers.CharField(source='placeId.placeName', read_only=True)

    class Meta:
        model = Plan
        fields = ['ceoId', 'renterId', 'placeId', 'name', 'phone', 'startDate', 'endDate', 'category', 'information', 'inquiry',
                  'approval']
