from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY
from django.db.models import Q

from django.core.paginator import Paginator


from .models import Event
from .serializers import EventSerializer

class EventAPIView(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('timestamp')
    serializer_class = EventSerializer
    http_method_names = ['get', 'head', 'post']

    @swagger_auto_schema(
        operation_description="Event List Endpoint",
        manual_parameters=[
            Parameter(
                'hotel_id', IN_QUERY,
                'the id of hotel',
                type='integer'),
            Parameter(
                'start_date', IN_QUERY,
                'the start date of the event',
                type='timestamp'),
            Parameter(
                'end_date', IN_QUERY,
                'the end date of the event',
                type='timestamp'),
            Parameter(
                'rpg_status', IN_QUERY,
                'the status of the event',
                type='integer'),
            Parameter(
                'room_id', IN_QUERY,
                'the id of the room',
                type='string'),
            Parameter(
                'start_date_stay', IN_QUERY,
                'the start date of stay',
                type='timestamp'),
            Parameter(
                'end_date_stay', IN_QUERY,
                'the end date of stay',
                type='timestamp'),
            Parameter(
                'limit', IN_QUERY,
                'limit number of displayed data',
                type='integer'),
            Parameter(
                'page', IN_QUERY,
                'page number of displayed data',
                type='integer'),
        ],
    )
    def list(self, request):
        query = request.GET
        limit = query.get("limit", 10)
        page_number = query.get("page", 1)
        query_search = query.get("search")

        queryset = self.get_queryset()
        
        db_query = Q()
        if query.get('hotel_id'):
            db_query &= Q(hotel_id=query.get('hotel_id'))

        if query.get('start_date'):
            db_query &= Q(timestamp__gte=query.get('start_date'))

        if query.get('end_date'):
            db_query &= Q(timestamp__lte=query.get('end_date'))

        status = query.get('rpg_status')
        if status:
            if status not in [1, 2, '1', '2']:
                return Response({"data": [], "msg": "invalid rpg_status", "error": True})
            db_query &= Q(rpg_status=status)

        if query.get('room_id'):
            db_query &= Q(room_id=query.get('room_id'))

        if query.get('start_date_stay'):
            db_query &= Q(night_of_stay__gte=query.get('start_date_stay'))

        if query.get('end_date_stay'):
            db_query &= Q(night_of_stay__lte=query.get('end_date_stay'))

        if len(db_query):
            queryset = Event.objects.filter(db_query).order_by('timestamp')

        paginator = Paginator(queryset, limit)
        result = paginator.get_page(page_number)
        serializer = EventSerializer(result, many=True)
        meta = {
            "page": int(page_number),
            "limit": int(limit),
            "totalPages": paginator.num_pages,
            "totalRecords": paginator.count
        }
        return Response({"data": serializer.data, "meta": meta})