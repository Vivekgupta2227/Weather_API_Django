
from django.conf.urls import url
from django.urls import path
from .views import WeatherListAPIView,Get_or_Post,get_with_temperature

from rest_framework.routers import DefaultRouter


urlpatterns = [
    url(r'^', view = WeatherListAPIView.as_view(), name = None),
    url(r'^weather$', view = Get_or_Post.as_view(), name = None),
    url(r'^weather/temperature$',view = get_with_temperature, name = None),
]