from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Place
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import base64
from django.core.files.base import ContentFile


class PlaceListView(APIView):
    def get(self, request, business, location):
        if business == 'total' and location == 'total':
            places = Place.objects.all()
        elif business == 'total':
            places = Place.objects.filter(location__in=location.split(','))
        elif location == 'total':
            places = Place.objects.filter(business__in=business.split(','))
        else:
            places = Place.objects.filter(business__in=business.split(','), location__in=location.split(','))
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlaceDetailView(APIView):
    def get(self, request, place_id):
        place = get_object_or_404(Place, pk=place_id)
        serializer = PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PlaceSerializer)
    def post(self, request):
        data = request.data
        serializer = PlaceSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(ceoId=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
