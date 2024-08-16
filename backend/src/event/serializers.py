from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'hotel_id',
            'room_id',
            'rpg_status',
            'night_of_stay',
            'timestamp',
        ]
