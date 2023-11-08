from django.urls import path
from .views import *

urlpatterns = [
    path('checklicense/<str:license_number>/', CheckLicenseView.as_view()),

    # path('dj/signup/<str:registration_type>/', CustomRegisterView.as_view(), name='custom_register'),
    # path("register/", RegisterAPIView.as_view()),

    path("register/<str:is_ceo>/", RegisterAPIView.as_view()),
    path('check-username/<str:username>/', CheckUsernameAPIView.as_view(), name='check-username'),
]