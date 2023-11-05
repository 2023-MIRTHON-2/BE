from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Place
from .serializers import PlaceListSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class PlaceListView(APIView):

    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PlaceListSerializer)
    def post(self, request):
        serializer = PlaceListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(presidentId=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        place = Place.objects.get(id=request.data['id'])
        place.delete()
        return Response(status=status.HTTP_200_OK)