from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class PlaceView(APIView):
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlaceListView(APIView):
    def get(self, request, business, location):
        if business == 'total' and location == 'total':
            places = Place.objects.all().order_by('-id')
        elif business == 'total':
            places = Place.objects.filter(location__in=location.split(',')).order_by('-id')
        elif location == 'total':
            places = Place.objects.filter(business__in=business.split(',')).order_by('-id')
        else:
            places = Place.objects.filter(business__in=business.split(','), location__in=location.split(',')).order_by(
                '-id')
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlaceDetailView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, place_id):
        place = get_object_or_404(Place, pk=place_id)
        serializer = PlaceSerializer(place)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PlaceSerializer)  # 이미지를 여러개 받을 수도 있다.
    def post(self, request):
        serializer = PlaceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(ceoId=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
