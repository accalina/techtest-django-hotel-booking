
def run_migrate_owner_os():
    from django.db import transaction
    from django.contrib.auth.models import User
    from django.db.models.functions import Length
    from src.event.models import Event
    from src.event.serializers import EventSerializer

    sid = transaction.savepoint()
    fileinput = open('scripts/sample_data.csv').read().strip().split('\n')
    room_reservation_id, night_of_stay, id, status, event_timestamp, hotel_id = fileinput[1].split(',')
    print(room_reservation_id,night_of_stay,id,status,event_timestamp,hotel_id)

    
    print(" [*] running data migration...")
    for index, row in enumerate(fileinput):
        room_reservation_id, night_of_stay, id, status, event_timestamp, hotel_id = fileinput[1].split(',')

        if index == 0:
            pass
        try:
            payload = {
                "hotel_id": hotel_id,
                "room_id": room_reservation_id,
                "rpg_status": status,
                "night_of_stay": night_of_stay,
                "timestamp": event_timestamp,
            }
            serialized_data = EventSerializer(data=payload)
            if not serialized_data.is_valid():
                print(f" [*] data in row {index+1} is not valid")
                continue
            serialized_data.save()
        except Exception as e:
            transaction.rollback(sid)
            print(e)
            break

    transaction.commit(sid)

# Run script
run_migrate_owner_os()