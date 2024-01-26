#!/usr/bin/python3
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone
from functools import lru_cache
from pathlib import Path
from typing import Dict

from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import db
from models import Store
from schemas.store import StoreView
from utils.csv_handler import CSVHandler

SOURCE_FOLDER: Path = Path("../input")
TIMEZONE_FILE: Path = Path.joinpath(SOURCE_FOLDER, "store_timezones.csv")
STATUS_FILE: Path = Path.joinpath(SOURCE_FOLDER, "store_status.csv")
WORKING_TIMES_FILE: Path = Path.joinpath(SOURCE_FOLDER, "store_working_times.csv")

CURRENT_DATETIME: datetime = datetime.now()


class StoreHandler(BaseModel):
    csv_results: Dict[str, dict]
    status_results: Dict[str, dict]

    @lru_cache()
    def get_data_from_csv(self) -> dict:
        """Returns a dictionary of store records"""
        csv_handler: CSVHandler = CSVHandler()
        csv_handler.read_timezones_from_csv(TIMEZONE_FILE)
        csv_handler.read_status_from_csv(STATUS_FILE)
        csv_handler.read_working_time_from_csv(WORKING_TIMES_FILE)
        self.csv_results = csv_handler.get_output_data
        return self.csv_results

    @lru_cache()
    def calculate_uptime(self) -> dict:
        """Returns a dictionary of store uptimes"""
        for store_id, values in self.results.items():
            store_timezone: timezone = values["timezone_str"]
            last_timestamp_utc: datetime = values["timestamp_utc"]
            last_timestamp_local: datetime = last_timestamp_utc.astimezone(
                store_timezone
            )
            store_open_time: time = values["start_time_local"]
            store_close_time: time = values["end_time_local"]
            store_status: str = values["status"]

            session: Session = next(db.session)
            store: StoreView = (
                session.query(Store).filter(Store.store_id == store_id).first()
            )
            if not store:
                raise Exception("Cannot get store object")

            uptime_hour: time
            uptime_day: time
            uptime_week: time
            downtime_hour: time
            downtime_day: time
            downtime_week: time

            # Check if store is Online
            if not store_status == "active":
                # Check if store is Open
                if store_open_time <= last_timestamp_local.time() <= store_close_time:
                    # Check last report timestamp against store hours
                    store.last_known_downtime_utc = CURRENT_DATETIME
                    downtime_hour = time(0, 60)
                    downtime_day = time(1)
                    downtime_week = time(1)
            else:
                store.last_known_uptime_utc = CURRENT_DATETIME
                if CURRENT_DATETIME.hour == store.last_known_uptime_utc.hour:
                    uptime_hour = timedelta(
                        CURRENT_DATETIME.min - store.last_known_uptime_utc.min
                    )
                else:
                    top_up_1 = abs(60 - timedelta(CURRENT_DATETIME.min))
                    top_up_2 = abs(60 - timedelta(store.last_known_uptime_utc.min))
                    uptime_hour = time(0, top_up_1 + top_up_2)
                if CURRENT_DATETIME.day == store.last_known_uptime_utc.day:
                    uptime_day = timedelta(
                        CURRENT_DATETIME.hour - store.last_known_uptime_utc.hour
                    )
                else:
                    top_up_1 = abs(24 - timedelta(CURRENT_DATETIME.hour))
                    top_up_2 = abs(24 - timedelta(store.last_known_uptime_utc.hour))
                    uptime_day = time(top_up_1 + top_up_2)
                if CURRENT_DATETIME.day - 7 <= store.last_known_uptime_utc.day:
                    uptime_week = timedelta(
                        CURRENT_DATETIME.hour - store.last_known_uptime_utc.hour
                    )
                else:
                    top_up_1 = abs(24 - timedelta(CURRENT_DATETIME.hour))
                    top_up_2 = abs(24 - timedelta(store.last_known_uptime_utc.hour))
                    uptime_week = time(top_up_1 + top_up_2)
            self.status_results[store_id]["uptime_last_hour"] = uptime_hour
            self.status_results[store_id]["uptime_last_day"] = uptime_day
            self.status_results[store_id]["uptime_last_week"] = uptime_week
            self.status_results[store_id]["downtime_last_hour"] = downtime_hour
            self.status_results[store_id]["downtime_last_day"] = downtime_day
            self.status_results[store_id]["downtime_last_week"] = downtime_week
            db.save(store)
        return self.status_results
