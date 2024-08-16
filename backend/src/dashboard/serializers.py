from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    period = serializers.IntegerField()
    count = serializers.IntegerField()
    period_type = serializers.CharField()
