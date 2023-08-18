#!/usr/bin/python3

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from celery import states
import time
import asyncio

from jobs.job_engine import generate_report_task
from models.report import Report
from db import db

router = APIRouter()

class ReportItem(BaseModel):
    id: str

class ResponseMessage(BaseModel):
    message: str

RESPONSES = {
    404: {"model": ResponseMessage, "description": "The item was not found"},
    200: {"description": "Id of the Item requested"},
}

@router.post("/trigger_report", response_model=ReportItem, responses={**RESPONSES})
def trigger_report():
    """Returns the report_id of the generated report object in the database"""
    try:
        report: Report = Report()
        db.save(report)
        report_id: str = str(report.report_id)
        print("Created report", report)
        generate_report_task.apply_async(args=[report_id])
        return {"id": report_id}
    except BaseException:
        return JSONResponse(status_code=404, content={"message": "Report generation failed."})

@router.get("/get_report/{report_id}")
def get_report(report_id: str):
    # Implement the logic to check the status of the report generation task.
    # If the task is still running, return "Running" with the Celery task state.
    # If the task is complete, return "Complete" along with the CSV file.

    task_result = generate_report_task.AsyncResult(report_id)
    if task_result.state == states.PENDING:
        return {"status": "Running", "task_state": task_result.state}
    elif task_result.state == states.SUCCESS:
        report_filename = task_result.get()
        # Return the generated CSV file as a response
        with open(report_filename, 'r') as report_file:
            csv_content = report_file.read()
        return {"status": "Complete", "csv_content": csv_content}
    else:
        # Task has failed or been revoked
        raise HTTPException(status_code=404, detail="Report not found")
    