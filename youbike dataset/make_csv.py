import json
import csv
import data_sorting

def json_to_csv_count(json_file, csv_file):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Set to collect all unique borrow_time values (for header columns)
    unique_times = set()
    # Dictionary mapping station name to another dictionary that maps borrow_time to event count.
    station_counts = {}

    for station_data in data:
        station_name = station_data["name"]
        events = station_data.get("borrow_events", [])
        counts = {}
        for event in events:
            bt = event["borrow_time"]
            counts[bt] = counts.get(bt, 0) + 1  # Count each event at that borrow time
            unique_times.add(bt)
        station_counts[station_name] = counts
    
    # Sort the times (assuming they are in a sortable format, e.g., "HH:MM")
    sorted_times = sorted(unique_times)

    # Write the CSV file.
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Header: first column is "station names", then each unique borrow_time
        header = ["station names"] + sorted_times
        writer.writerow(header)
        
        # Write one row per station.
        for station_name, counts in station_counts.items():
            row = [station_name]
            for t in sorted_times:
                # Write the count if available; if no event, use 0.
                row.append(counts.get(t, 0))
            writer.writerow(row)

# Example usage:
if __name__ == "__main__":
    data_sorting.csv_to_json("202312_轉乘YouBike2.0票證刷卡資料.csv", "202312_sorted.json")
    json_to_csv_count("202312_sorted.json", "202312.csv")
    