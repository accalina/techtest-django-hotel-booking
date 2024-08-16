from django.db import models

# Create your models here.
class Event(models.Model):
    hotel_id = models.IntegerField()
    room_id = models.CharField(max_length=60)
    rpg_status = models.IntegerField()
    night_of_stay = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural  = 'Events'
        db_table = 'event'

    def __str__(self):
        return f"event: {self.id}, hotel_id: {self.hotel_id}"