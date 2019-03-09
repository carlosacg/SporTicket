from rest_framework import serializers
from apps.events.models import Event

class EventSerializers(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'initial_date', 'initial_time', 'place', 'url','state', 'capacity', 'visitor', 'local', 'image','event_type') 