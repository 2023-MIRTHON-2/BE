from django.urls import path
from .views import *

urlpatterns = [
    path('checklicense/', CheckLicenseView.as_view()),

]

#dkdk
