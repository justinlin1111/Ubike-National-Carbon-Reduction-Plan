def data_transform(csv_file, output_csv_file):
    from collections import defaultdict
    import csv
    from datetime import datetime
    
    # Dictionary to store net flow of bikes at each station per hour.
    station_net_flow = defaultdict(lambda: defaultdict(int))
    hour_to_weekday = {}  # 紀錄每個小時對應的星期幾
    unique_hours = set()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Uncomment the next line if your CSV file contains a header.
        next(reader, None)
        for row in reader:
            # Extract values based on column indices:
            borrow_time   = row[0]  # e.g., "2023-12-16T23:00:00+08:00"
            borrow_station = row[1]  # e.g., "台大" (borrow station)
            return_time   = row[2]  # e.g., "2023-12-16T23:00:00+08:00"
            return_station = row[3]  # e.g., "公館" (return station)
            
            # 取得星期幾
            borrow_date = borrow_time.split("T")[0]  # "YYYY-MM-DD"
            return_date = return_time.split("T")[0]

            borrow_weekday = datetime.strptime(borrow_date, "%Y-%m-%d").strftime("%A")
            return_weekday = datetime.strptime(return_date, "%Y-%m-%d").strftime("%A")

            # 儲存對應的星期幾 (避免重複計算)
            hour_to_weekday[borrow_time] = borrow_weekday
            hour_to_weekday[return_time] = return_weekday

            # Decrease bike count at borrow station
            station_net_flow[borrow_station][borrow_time] -= 1
            unique_hours.add(borrow_time)
            
            # Increase bike count at return station
            station_net_flow[return_station][return_time] += 1
            unique_hours.add(return_time)
    
    # Sort the hours (assuming they are in a sortable format "YYYY-MM-DDTHH")
    sorted_hours = sorted(unique_hours)
    
    # Write the output CSV file.
    with open(output_csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Header: first column is "station names", then each unique hour
        header = ["station names"] + sorted_hours
        writer.writerow(header)
        
        # **第二行：對應的星期幾**
        weekday_row = ["weekday"] + [hour_to_weekday.get(hour, "Unknown") for hour in sorted_hours]
        writer.writerow(weekday_row)

        # Write one row per station.
        for station_name, counts in station_net_flow.items():
            row = [station_name]
            for hour in sorted_hours:
                # Write the net flow count if available; if no event, use 0.
                row.append(counts.get(hour, 0))
            writer.writerow(row)