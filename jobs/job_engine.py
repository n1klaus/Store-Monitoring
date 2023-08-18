#!/usr/bin/python3
from pathlib import Path

from celery import Celery

from core.settings import get_settings
from models.store import Store
from utils.csv_handler import CSVHandler

settings = get_settings()

OUTPUT_PATH = Path("../output/")

CELERY_RESULT_BACKEND = "db+" + settings.DATABASE_URL

celery = Celery(
    "tasks", broker=settings.CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND
)


@celery.task(bind=True)
def generate_report_task(self, report_id):
    print("here!!")
    try:
        from db import db

        session = next(db.session)

        # Fetch the required data from the database using SQLAlchemy
        stores = session.query(Store).all()
        print("Found stores: ", stores)
        # Process the data and generate the report
        report_data = {store.store_id: store.get_online_stats() for store in stores}
        print("Report Data: ", report_data)

        # Write the generated report to a CSV file
        report_filename = OUTPUT_PATH.joinpath(f"report_{report_id}.csv")
        print("Report Filename: ", report_filename)
        CSVHandler.generate_report(report_data, report_filename)

        return report_filename  # Return the filename of the generated report
    except Exception as e:
        # Handle any exceptions that might occur during report generation
        print("Error found", e)
        self.update_state(state="FAILURE", meta={"error_message": str(e)})
        raise
    finally:
        session.close()
