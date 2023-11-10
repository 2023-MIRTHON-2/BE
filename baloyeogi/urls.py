from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls import url

from rest_framework import routers
from rest_framework import permissions


from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi


# router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="제목 작성",
        default_version='v1',
        description="설명 작성",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="wewqwew153@gmail.com"),
        license=openapi.License(name=""),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    # patterns=schema_url_patterns,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('places/', include('places.urls')),
    path('plans/', include('plans.urls')),
    path('dj/', include('dj_rest_auth.urls')),
    path('dj/signup/', include('dj_rest_auth.registration.urls')),


    url(r'^swagger(?P<format>\.json|\.yaml)/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
