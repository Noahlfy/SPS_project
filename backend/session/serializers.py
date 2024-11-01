from rest_framework import serializers
import threading
from .models import Session

from .services import start_mqtt_clients, stop_mqtt_clients, close_mqtt_clients

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = '__all__'


    def create(self, validated_data):
        Session.objects.all().update(status='completed')
        # close_mqtt_clients()
        session = Session.objects.create(**validated_data)
        start_mqtt_clients(session.session_id)
        return session

    def update(self, instance, validated_data):
        status = validated_data.get('status', None)
        if instance.status == 'completed':
            raise serializers.ValidationError('Session is already completed')
        if status == 'active':
            start_mqtt_clients(instance.session_id)
        if status == 'paused':
            stop_mqtt_clients()
        elif status == 'completed':
            close_mqtt_clients()
        return super().update(instance, validated_data)
