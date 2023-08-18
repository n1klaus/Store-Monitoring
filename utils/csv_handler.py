#!/usr/bin/python3

import csv
import pytz
from dateutil import parser
from datetime import datetime, time, timezone
from pydantic import BaseModel
from pathlib import Path
from typing import Dict
from collections import defaultdict

class CSVHandler(BaseModel):
    _output: Dict[str, dict] = defaultdict(dict)
    _save_file: Path = Path('./output/report.csv')

    @property
    def get_output_data(self):
        """Returns the output dictionary"""
        return self._output
    
    @property
    def get_saved_file(self):
        """Returns the save file path"""
        return self._save_file
    
    def read_timezones_from_csv(self, read_file: Path) -> None:
        """Updates with key-value pair of store_id and respective timezone"""
        with open(read_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id: str = row['store_id']
                timezone_str: timezone = pytz.timezone(row['timezone_str'])
                self._output[store_id].update({'timezone_str': timezone_str})

    def read_working_time_from_csv(self, read_file: Path) -> None:
        """Updates with key-value pair of store_id and respective working times"""
        with open(read_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                store_id: str = row['store_id']
                day_of_week: int = int(row['day'])
                start_time_local: time = time(*map(int, row['start_time_local'].split(":")))
                end_time_local: time = time(*map(int, row['end_time_local'].split(':')))
                self._output[store_id].update(**{
                    'day_of_week': day_of_week,
                    'start_time_local': start_time_local,
                    'end_time_local': end_time_local,
                })

    def read_status_from_csv(self, read_file: Path) -> None:
        """Updates with key-value pair of store_id and respective online/offine status"""
        with open(read_file, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id: str = row['store_id']
                status: str = row['status']
                timestamp_utc: datetime = parser.parse(row['timestamp_utc'])
                self._output[store_id].update({
                    'status': status,
                    'timestamp_utc': timestamp_utc,
                })

    def generate_report(self, report_data: dict) -> None:
        """Writes the final report to a CSV file"""
        with open(self._save_file, 'w', encoding='utf-8', newline='') as csvfile:
            fieldnames = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week',
                        'downtime_last_hour', 'downtime_last_day', 'downtime_last_week']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
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
