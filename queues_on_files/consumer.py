# consumer.py - obsługuje kolejkę z pliku CSV
import csv
import time
import os
from datetime import datetime

QUEUE_FILE = 'queue.csv'
TASK_DURATION = 30  # sekund
CHECK_INTERVAL = 5  # sekund

def process_task(row):
    print(f"Rozpoczynam zadanie: {row[1]} (id: {row[0]})")
    time.sleep(TASK_DURATION)
    print(f"Zakończono zadanie: {row[1]} (id: {row[0]})")

def consume():
    while True:
        if not os.path.exists(QUEUE_FILE):
            time.sleep(CHECK_INTERVAL)
            continue
        rows = []
        updated = False
        with open(QUEUE_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = list(csv.reader(file))
        for row in reader:
            if row[2] == 'pending' and not updated:
                row[2] = 'in_progress'
                row.append(datetime.now().isoformat())
                updated = True
                process_task(row)
                row[2] = 'done'
                row.append(datetime.now().isoformat())
            rows.append(row)
        if updated:
            with open(QUEUE_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    consume()