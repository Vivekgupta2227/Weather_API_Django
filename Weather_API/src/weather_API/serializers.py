from rest_framework.serializers import ModelSerializer
from .models import (Location,
                     weather_data
                     )

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class WeatherDataSerializer(ModelSerializer):
    location = LocationSerializer(required=True)

    class Meta:
        model = weather_data
        fields = '__all__'

    def create(self, validated_data):
        loc_data = validated_data.pop('location', None)
        location = Location.objects.create(**loc_data)
        return weather_data.objects.create(location=location, **validated_data)


    def update(self, instance, validated_data):
        loc_dict = validated_data.pop('location', None)
        if loc_dict:
            loc_obj = instance.location
            for key, value in loc_dict.iteritems():
                setattr(loc_obj, key, value)
            loc_obj.save()
            validated_data["location"] = loc_obj
        for key, value in validated_data.iteritems():
            setattr(instance, key, value)
        instance.save()
        return instance