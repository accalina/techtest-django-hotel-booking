from django.shortcuts import render
from django.db.models import Q, F
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema

from src.event.models import Event
from .serializers import DashboardSerializer

# Create your views here.

class DashboardAPIView(ViewSet):

    @swagger_auto_schema(
        operation_description="Event List Endpoint",
        manual_parameters=[
            Parameter(
                'hotel_id', IN_QUERY,
                'the id of hotel',
                required=True,
                type='integer'),
            Parameter(
                'period_type', IN_QUERY,
                'the type of period: `day` or `month` or `year`',
                required=True,
                type='string'),
            Parameter(
                'month', IN_QUERY,
                'the filter for month',
                type='integer'),
            Parameter(
                'year', IN_QUERY,
                'the filter for year',
                type='integer'),
        ],
    )
    def list(self, request):
        query = request.GET
        hotel_id = query.get("hotel_id")
        period_type = query.get("period_type").lower()
        month = query.get("month")
        year = query.get("year")

        query_db = Q(hotel_id=hotel_id)
        if month:
            if not 0 < int(month) < 13:
                return Response({"message": "invalid month", "data": [], "error": True})
            query_db &= Q(night_of_stay__month=month)
        if year:
            query_db &= Q(night_of_stay__year=year)

        result = Event.objects.filter(query_db)        
        if period_type == 'day':
            data = result.values('night_of_stay__day').annotate(count=Count('id'))
        elif period_type == 'month':
            data = result.values('night_of_stay__month').annotate(count=Count('id'))
        elif period_type == 'year':
            data = result.values('night_of_stay__year').annotate(count=Count('id'))
        else:
            return Response({"message": "invalid period_type", "data": [], "error": True})

        for entry in data:
            entry['period_type'] = period_type
            entry['period'] = entry.pop('night_of_stay__' + period_type)

        serialized_data = DashboardSerializer(data, many=True).data
        return Response({"data": serialized_data})

