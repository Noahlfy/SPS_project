from rest_framework import serializers
import threading
from .models import Session

from .services import start_mqtt_clients, stop_mqtt_clients, close_mqtt_clients

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = '__all__'


    def create(self, validated_data):
        start_mqtt_clients()
        return Session.objects.create(**validated_data)

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        if status == 'paused':
            stop_mqtt_clients()
        elif status == 'completed':
            close_mqtt_clients()
        return super().update(instance, validated_data)
