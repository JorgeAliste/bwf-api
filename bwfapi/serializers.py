from rest_framework import serializers
from .models import Group, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'team_1', 'team_2', 'time', 'score_1', 'score_2', 'group')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'location', 'description')


class GroupFullSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'location', 'description', 'events')
