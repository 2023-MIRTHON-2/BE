from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404
from .models import User, Place, Plan
from .serializers import PlanSerializer, PlanShowSerializer, PlanRenterShowSerializer, PlanCeoShowSerializer, ApprovalContractSerializer, ContractShowSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class IsAuthenticatedAndNotCEO(permissions.BasePermission):
    """
    커스텀 권한을 검사하여, 인증된 사용자 중 is_ceo가 False인 사용자만 허용합니다.
    """

    def has_permission(self, request, view):
        # 사용자가 로그인했는지와 is_ceo가 False인지 확인합니다.
        return request.user and request.user.is_authenticated and not request.user.is_ceo


class PlanCreate(generics.CreateAPIView):
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticatedAndNotCEO]  # 로그인한 사용자만 접근 가능하도록 설정

    def get_serializer_context(self):
        context = super(PlanCreate, self).get_serializer_context()
        # URL에서 ceo_Id를 가져옵니다.
        context['place_id'] = self.kwargs['place_Id']
        # 현재 로그인한 사용자의 ID를 renter_id로 설정합니다.
        context['renter_id'] = self.request.user.id
        return context

    def perform_create(self, serializer):
        renter_id = self.get_serializer_context().get('renter_id')
        place_id = self.get_serializer_context().get('place_id')
        renter = get_object_or_404(User, pk=renter_id)
        place = get_object_or_404(Place, pk=place_id)
        ceo = place.ceoId

        print(renter)
        print(ceo)
        print(place)
        # 'ceoId'와 'renterId'를 각각 CEO와 현재 로그인한 사용자로 설정하여 저장합니다.
        serializer.save(ceoId=ceo, renterId=renter, placeId=place)


class PlanShow(generics.RetrieveAPIView):
    serializer_class = PlanShowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        plan_id = self.kwargs.get('plan_Id')
        return get_object_or_404(Plan, pk=plan_id)


class PlanApprovalUpdate(generics.UpdateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        plan_id = self.kwargs.get('plan_Id')
        return get_object_or_404(Plan, pk=plan_id)

    def patch(self, request, *args, **kwargs):
        plan = self.get_object()
        plan.approval = True
        plan.save()
        return Response({"status": "approval 필드 True 설정"}, status=status.HTTP_200_OK)


class PlansRenterList(generics.ListAPIView):
    serializer_class = PlanRenterShowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        현재 로그인한 사용자가 renterId인 Plan 객체를 필터링합니다.
        """
        user = self.request.user
        return Plan.objects.filter(renterId=user)


class PlansCeoList(generics.ListAPIView):
    serializer_class = PlanCeoShowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        현재 로그인한 사용자가 CEO이며, URL 파라미터로 주어진 place_Id와 관련된 Plan 객체만 필터링합니다.
        """
        user = self.request.user
        place_id = self.kwargs['place_Id']
        return Plan.objects.filter(ceoId=user, placeId=place_id, approval=True)


class ContractShow(generics.RetrieveAPIView):
    serializer_class = ContractShowSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        plan_id = self.kwargs.get('plan_Id')
        return get_object_or_404(Plan, pk=plan_id)


class MypageList(generics.ListAPIView):
    serializer_class = ApprovalContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        현재 로그인한 사용자가 CEO이며, URL 파라미터로 주어진 place_Id와 관련된 Plan 객체만 필터링합니다.
        """
        user = self.request.user
        return Plan.objects.filter(ceoId=user, approval=True)