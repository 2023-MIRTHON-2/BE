from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import User, Place
from .serializers import PlanSerializer
from rest_framework.permissions import IsAuthenticated


class PlanCreate(generics.CreateAPIView):
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능하도록 설정

    def get_serializer_context(self):

        context = super(PlanCreate, self).get_serializer_context()
        # URL에서 ceo_Id를 가져옵니다.
        context['place_id']= self.kwargs['place_Id']
        # 현재 로그인한 사용자의 ID를 renter_id로 설정합니다.
        context['renter_id'] = self.request.user.id
        return context

    def perform_create(self, serializer):
        renter_id = self.get_serializer_context().get('renter_id')
        place_id = self.get_serializer_context().get('place_id')
        renter = get_object_or_404(User, pk=renter_id)
        place = get_object_or_404(Place, pk=place_id)
        ceo = place.presidentId

        print(renter)
        print(ceo)
        print(place)
        # 'ceoId'와 'renterId'를 각각 CEO와 현재 로그인한 사용자로 설정하여 저장합니다.
        serializer.save(ceoId=ceo, renterId=renter, placeId=place)

