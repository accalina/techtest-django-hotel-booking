from django.contrib import admin
from .models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display    = [
        'hotel_id',
        'room_id',
        'rpg_status',
        'night_of_stay',
        'timestamp',
        'updated',
    ]
    list_filter     = ['rpg_status']
    search_fields   = ['hotel_id']
    ordering        = ['timestamp']
    list_per_page   = 20

admin.site.register(Event, EventAdmin)