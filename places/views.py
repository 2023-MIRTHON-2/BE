from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializer, LocationPlaceSerializer


# 가. 공간 정보 조회
# 1. 공간 정보 리스트 조회
class PlaceListView(APIView):
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


# 2. 메인페이지용 공간 정보 리스트 조회(location, category, placeName, placeImageUrl. cost)
# location으로 필터링
class LocationPlaceListView(APIView):
    def get(self, request, location):
        places = Place.objects.filter(location=location)
        serializer = LocationPlaceSerializer(places, many=True)
        return Response(serializer.data)





# 나. 공간 정보 등록
# 1. 사업자 등록 번호 검색
# 2. 임대차 계약서
