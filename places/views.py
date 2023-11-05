from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Place
from .serializers import PlaceListSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class MakePlaceListView(APIView):

    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlaceListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(presidentId=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)


class PlaceListView(APIView):
    # 위치와 카테고리를 받아서 해당하는 사업장을 보여준다. 위키와 카테고리는 각각 all이 들어오면, 모든 사업장을 보여준다.
    def get(self, request, category, location):
        if category == 'all' and location == 'all':
            places = Place.objects.all()
        elif category == 'all':
            places = Place.objects.filter(location=location)
        elif location == 'all':
            places = Place.objects.filter(category=category)
        else:
            places = Place.objects.filter(category=category, location=location)
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)


class PlaceDetailView(APIView):
    @swagger_auto_schema(request_body=PlaceListSerializer)
    def delete(self, request, post_id):
        place = get_object_or_404(Place, pk=post_id)
        place.delete()
        return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
