from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,CreateAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404,HttpResponse
from datetime import datetime
from rest_framework.decorators import api_view

from .models import weather_data,Location
from.serializers import WeatherDataSerializer
import sys
# Create your views here.

class WeatherListAPIView(ListCreateAPIView):
    queryset = weather_data.objects.all()
    serializer_class = WeatherDataSerializer

class Get_or_Post(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
       
        if request.method == 'GET':
            if request.GET.get('lat') is None and request.GET.get('lon') is None:
                qs = weather_data.objects.all.order_by('id')
                serializer = WeatherDataSerializer(qs, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
               
            else:
                lat = float(request.GET.get('lat'))
                lon = float(request.GET.get('lon'))
                qs = weather_data.objects.filter(location__lat=lat, location__lon=lon)
                qs = get_object_or_404(qs)
                serializer = WeatherDataSerializer(qs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
                

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = WeatherDataSerializer(data=request.data)
            if serializer.is_valid():
                w_data = serializer.save()
                serializer = WeatherDataSerializer(w_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_with_temperature(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if request.method == 'GET':
        sd = request.GET.get('start')
        ed = request.GET.get('end')
        sd = datetime.strptime(sd, '%Y-%m-%d').date()
        ed = datetime.strptime(ed, '%Y-%m-%d').date()
        queryset = weather_data.objects.filter(date__range=[sd, ed])
        data = []
        for q in queryset:
            ht = sys.float_info.min
            lt = sys.float_info.max
            for t in q.temperature:
                if t < lt :
                    lt = t
                if t > ht :
                    ht = t
            dict = {

                'lat': q.location.lat,
                'lon': q.location.lon,
                'city': q.location.city,
                'state': q.location.state,
                'lowest': lt,
                'highest': ht,
            }
            data.append(dict)
        return Response(data, status=status.HTTP_200_OK)
