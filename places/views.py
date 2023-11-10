from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from baloyeogi import settings
from .models import Place
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import requests

API_KEY = settings.API_KEY


class CheckLicenseView(APIView):

    # 사업자 등록번호 유효한지 확인
    def get(self, request, license_number):
        api_url = f'https://bizno.net/api/fapi?key={API_KEY}&gb=1&q={license_number}&type=json&pagecnt=1'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
            data = response.json()
            items = data.get('items', [])
            if items:
                company_data = items[0]  # 첫 번째 회사 정보를 가져옵니다.
                company_name = company_data.get('company', '')
                if company_name:  # 유효한 사업자 등록 번호인 경우
                    return Response({'message': f'{company_name}: 유효한 사업자 등록 번호입니다.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': '유효하지 않은 사업자 등록 번호입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({'error': 'API 호출 중 오류 발생'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlaceView(APIView):
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
