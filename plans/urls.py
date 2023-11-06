from django.urls import path
from .views import PlanCreate, PlanShow, PlanApprovalUpdate, PlansRenterList, PlansCeoList

urlpatterns = [
    # path("create/<int:ceo_Id>/<int:place_Id>/", PlanCreate.as_view(), name='plan-create'),
    path("create/<int:place_Id>/", PlanCreate.as_view(), name='plan-create'),
    path("show/<int:plan_Id>/", PlanShow.as_view(), name='plan-show'),
    path('approval/<int:plan_Id>/', PlanApprovalUpdate.as_view(), name='plan-approval-update'),
    path('renter/list/', PlansRenterList.as_view(), name='plan-renter-list'),
    path('ceo/list/<int:place_Id>/', PlansCeoList.as_view(), name='plan-ceo-list'),
]
