from django.urls import path
from .views import PlanCreate

urlpatterns = [
    # path("create/<int:ceo_Id>/<int:place_Id>/", PlanCreate.as_view(), name='plan-create'),
    path("create/<int:place_Id>/", PlanCreate.as_view(), name='plan-create'),
]
