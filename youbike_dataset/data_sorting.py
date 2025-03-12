import csv
import json
from collections import defaultdict

def csv_to_json(csv_file, json_file):
    # Dictionary to group events by borrow station.
    station_events = defaultdict(list)
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Uncomment the next line if your CSV file contains a header.
        # next(reader, None)
        for row in reader:
            # Extract values based on column indices:
            borrow_time   = row[0]  # e.g., "2023-12-16T23:00:00+08:00"
            station_name  = row[1]  # e.g., "捷運公館站(2號出口)" (borrow station)
            return_time   = row[2]  # e.g., "2023-12-16T23:00:00+08:00"
            use_time      = row[4]  # e.g., "00:04:56"
            borrow_date   = row[5]  # e.g., "2023-12-16"
            
            # Build the borrow event dictionary.
            event = {
                "borrow_time": borrow_time,
                "return_time": return_time,
                "use_time": use_time,
                "borrow_date": borrow_date
            }
            
            # Append the event to the corresponding station.
            station_events[station_name].append(event)
    
    # Build the JSON structure: an array of station_data objects.
    json_data = []
    for station, events in station_events.items():
        json_data.append({
            "name": station,
            "borrow_events": events
        })
    
    # Write the output to a JSON file.
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)