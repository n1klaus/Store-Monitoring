#!/usr/bin/python3

import csv
import pytz
from dateutil import parser
from datetime import datetime, time
from pydantic import BaseModel
from pathlib import Path

class CSVHandler(BaseModel):
    output: dict = {}
    save_file: Path = Path('./output/report.csv')

    def read_timezones_from_csv(self, read_file, output_file = output) -> dict:
        """Returns key-value pair of store_id and respective timezone"""
        with open(read_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id: str = row['store_id']
                timezone_str = pytz.timezone(row['timezone_str'])
                output_file[store_id] = timezone_str
        return output_file

    def read_working_time_from_csv(self, read_file, output_file = output) -> dict:
        """Returns key-value pair of store_id and respective working times"""
        with open(read_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                store_id: str = row['store_id']
                day_of_week: int = int(row['day'])
                start_time_local: time = time(*map(int, row['start_time_local'].split(":")))
                end_time_local: time = time(*map(int, row['end_time_local'].split(':')))
                output_file[store_id] = {
                    'day_of_week': day_of_week,
                    'start_time_local': start_time_local,
                    'end_time_local': end_time_local,
                }
        return output_file

    def read_status_from_csv(self, read_file, output_file = output):
        with open(read_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id: str = row['store_id']
                status: str = row['status']
                timestamp_utc: datetime = parser.parse(row['timestamp_utc'])
                output_file[store_id] = {
                    'status': status,
                    'timestamp_utc': timestamp_utc,
                }
        return output_file

    def generate_report(self, report_data, read_file, output_file = save_file):
        with open(read_file, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week',
                        'downtime_last_hour', 'downtime_last_day', 'downtime_last_week']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            for store_id, store_stats in report_data.items():
                writer.writerow({
                    'store_id': store_id,
                    'uptime_last_hour': store_stats['uptime_last_hour'],
                    'uptime_last_day': store_stats['uptime_last_day'],
                    'uptime_last_week': store_stats['uptime_last_week'],
                    'downtime_last_hour': store_stats['downtime_last_hour'],
                    'downtime_last_day': store_stats['downtime_last_day'],
                    'downtime_last_week': store_stats['downtime_last_week'],
                })
