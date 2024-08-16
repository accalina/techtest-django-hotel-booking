
import json
import requests

filename = 'sample_data.csv'


def main():
    fileinput = open(filename).read().strip().split('\n')

    for index, row in enumerate(fileinput):
        room_reservation_id, night_of_stay, id, status, event_timestamp, hotel_id = row.split(',')
        if index == 0:
            pass
        result = requests.post('http://localhost:8000/event/', json={
            "hotel_id": hotel_id,
            "room_id": room_reservation_id,
            "rpg_status": status,
            "night_of_stay": night_of_stay,
            "timestamp": event_timestamp,
        })
        if result.status_code != 201:
            print(f" [x] error on csv row: {index+1}")
            break
        else:
            print(f" [*] {index} - {result.status_code}")

main()