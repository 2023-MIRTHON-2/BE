from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializer


# 가. 공간 정보 조회
# 1. 공간 정보 리스트 조회
# class PlaceListView(APIView):
#     def get(self, request):
#         places = Place.objects.all()
#         serializer = PlaceSerializer(places, many=True)
#         return Response(serializer.data)


# 2. 상세 공유공간 찾기용 공간 정보 리스트 조회(location, category, placeName, placeImageUrl. cost)
# location과 category를 받아서 해당하는 공간 정보 리스트를 반환. location과 category는 각각 '전체'일 수도 있음.
class FilterPlaceListView(APIView):
    def get(self, request, location, category):
        if location == '전체' and category == '전체':
            places = Place.objects.all()
        elif location == '전체':
            places = Place.objects.filter(category=category)
        elif category == '전체':
            places = Place.objects.filter(location=location)
        else:
            places = Place.objects.filter(location=location, category=category)
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    # 목데이터용 임시 post 메서드
    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

# 나. 공간 정보 등록
# 1. 사업자 등록 번호 검색
# 2. 임대차 계약서
