from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY

from django.core.paginator import Paginator


from .models import Event
from .serializers import EventSerializer

class EventAPIView(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('timestamp')
    serializer_class = EventSerializer
    search_fields = ['timestamp']
    filter_backends = [SearchFilter]
    http_method_names = ['get', 'head', 'post']

    @swagger_auto_schema(
        operation_description="Sales Order List Endpoint",
        manual_parameters=[
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
        if query_search:
            queryset = self.filter_queryset(self.get_queryset())

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