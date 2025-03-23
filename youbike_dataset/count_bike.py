import csv
import os
from collections import defaultdict
from datetime import datetime

def csv_to_hourly_rent_count(csv_file, output_csv_file):
    # Dictionary to group return events by station and hour.
    station_counts = defaultdict(lambda: defaultdict(int))
    hour_to_weekday = {}  # 紀錄每個小時對應的星期幾
    unique_hours = set()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Uncomment the next line if your CSV file contains a header.
        next(reader, None)
        for row in reader:
            # Extract values based on column indices:
            rent_time   = row[0]  # e.g., "2023-12-16T23:00:00+08:00"
            rent_station = row[1]  # e.g., "台大" (rent station)
            
            # 取得星期幾
            rent_date = rent_time.split("T")[0]  # "YYYY-MM-DD"

            rent_weekday = datetime.strptime(rent_date, "%Y-%m-%d").strftime("%A")

            hour_to_weekday[rent_time] = rent_weekday

            # Increment the count for the return station at that hour.
            station_counts[rent_station][rent_time] += 1
            unique_hours.add(rent_time)
    
    # Sort the hours (assuming they are in a sortable format "YYYY-MM-DDTHH")
    sorted_hours = sorted(unique_hours)
    
    # Write the output CSV file.
    with open(output_csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Header: first column is "station names", then each unique return hour
        header = ["station names"] + sorted_hours
        writer.writerow(header)

        # **第二行：對應的星期幾**
        weekday_row = ["weekday"] + [hour_to_weekday.get(hour, "Unknown") for hour in sorted_hours]
        writer.writerow(weekday_row)
        
        # Write one row per station.
        for station_name, counts in station_counts.items():
            row = [station_name]
            for hour in sorted_hours:
                # Write the count if available; if no event, use 0.
                row.append(counts.get(hour, 0))
            writer.writerow(row)

def csv_to_hourly_return_count(csv_file, output_csv_file):
    # Dictionary to group return events by station and hour.
    station_counts = defaultdict(lambda: defaultdict(int))
    hour_to_weekday = {}  # 紀錄每個小時對應的星期幾
    unique_hours = set()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Uncomment the next line if your CSV file contains a header.
        next(reader, None)
        for row in reader:
            # Extract values based on column indices:
            return_time   = row[2]  # e.g., "2023-12-16T23:00:00+08:00"
            return_station = row[3]  # e.g., "台大" (return station)
            
            # 取得星期幾
            return_date = return_time.split("T")[0]

            return_weekday = datetime.strptime(return_date, "%Y-%m-%d").strftime("%A")

            hour_to_weekday[return_time] = return_weekday

            # Increment the count for the return station at that hour.
            station_counts[return_station][return_time] += 1
            unique_hours.add(return_time)
    
    # Sort the hours (assuming they are in a sortable format "YYYY-MM-DDTHH")
    sorted_hours = sorted(unique_hours)
    
    # Write the output CSV file.
    with open(output_csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Header: first column is "station names", then each unique return hour
        header = ["station names"] + sorted_hours
        writer.writerow(header)
        
        # **第二行：對應的星期幾**
        weekday_row = ["weekday"] + [hour_to_weekday.get(hour, "Unknown") for hour in sorted_hours]
        writer.writerow(weekday_row)

        # Write one row per station.
        for station_name, counts in station_counts.items():
            row = [station_name]
            for hour in sorted_hours:
                # Write the count if available; if no event, use 0.
                row.append(counts.get(hour, 0))
            writer.writerow(row)

def csv_to_hourly_net_flow(csv_file, output_csv_file):
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


if __name__ == "__main__":
    for i in range(1, 12+1):
        # 確保資料夾存在，不存在會直接創建資料夾
        os.makedirs(r"raw_data_json", exist_ok=True)
        os.makedirs(r"processed_data_rent", exist_ok=True)
        os.makedirs(r"processed_data_return", exist_ok=True)
        os.makedirs(r"net_flow_data", exist_ok=True)

        csv_to_hourly_return_count(
            r"raw_data_csv\2023" + str(i).zfill(2) + "_轉乘YouBike2.0票證刷卡資料.csv",
            r"processed_data_rent\2023" + str(i).zfill(2) + ".csv"
        )

        csv_to_hourly_return_count(
            r"raw_data_csv\2023" + str(i).zfill(2) + "_轉乘YouBike2.0票證刷卡資料.csv",
            r"processed_data_return\2023" + str(i).zfill(2) + ".csv"
        )

        csv_to_hourly_net_flow(
            r"raw_data_csv\2023" + str(i).zfill(2) + "_轉乘YouBike2.0票證刷卡資料.csv",
            r"net_flow_data\2023" + str(i).zfill(2) + ".csv"
        )


    