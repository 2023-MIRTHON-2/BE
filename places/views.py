from django.shortcuts import render
from rest_framework.views import APIView

# 가. 공간 정보 조회
# 1. 공간 정보 리스트 조회
class PlaceListView(APIView):
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


# 2. 공간 정보 상세 조회





# 나. 공간 정보 등록
# 1. 사업자 등록 번호 검색
# 2. 임대차 계약서
