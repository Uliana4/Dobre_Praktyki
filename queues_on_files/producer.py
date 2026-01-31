# producer.py - dodaje zadania do kolejki (plik CSV)
import csv
import uuid
from datetime import datetime

QUEUE_FILE = 'queue.csv'

def add_task(description):
    with open(QUEUE_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            str(uuid.uuid4()),
            description,
            'pending',
            datetime.now().isoformat()
        ])

if __name__ == "__main__":
    for i in range(1, 101):
        add_task(f"Rozmowa telefoniczna {i}")
    print("Dodano 100 zadań do kolejki.")