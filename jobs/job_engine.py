#!/usr/bin/python3
from pathlib import Path

from config import celery
from db import db
from models import Store
from utils.csv_handler import CSVHandler

OUTPUT_PATH = Path("../output/")


@celery.task(bind=True, name="report_task")
def generate_report_task(self):
    print("here!!")
    try:
        session = next(next(db).session)

        # Fetch the required data from the database using SQLAlchemy
        stores = session.query(Store).all()
        print("Found stores: ", stores)
        # Process the data and generate the report
        report_data = {store.store_id: store.get_online_stats() for store in stores}
        print("Report Data: ", report_data)

        # Write the generated report to a CSV file
        report_filename = OUTPUT_PATH.joinpath(f"report_{self.id}.csv")
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
