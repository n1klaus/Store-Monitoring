#!/usr/bin/python3
from pprint import pprint

from celery import states
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import celery
from jobs.job_engine import generate_report_task

router = APIRouter()


class ReportItem(BaseModel):
    id: str


class ResponseMessage(BaseModel):
    message: str


RESPONSES = {
    404: {"model": ResponseMessage, "description": "The item was not found"},
    200: {"description": "Id of the Item requested"},
}

RETRY_POLICY: dict = {
    "interval_start": 0,
    "interval_step": 0.2,
    "interval_max": 0.2,
    "max_retries": 5,
}


@router.post("/trigger_report", response_model=ReportItem, responses={**RESPONSES})
def trigger_report():
    """Returns the task id of the generated report task"""
    try:
        report_task = generate_report_task.apply_async(
            args=(), retry=True, retry_policy=RETRY_POLICY
        )
        return {"id": report_task.id}
    except BaseException:
        return JSONResponse(
            status_code=404, content={"message": "Report generation failed."}
        )


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
        with open(report_filename, "r") as report_file:
            csv_content = report_file.read()
        return {"status": "Complete", "csv_content": csv_content}
    else:
        # Task has failed or been revoked
        raise HTTPException(status_code=404, detail="Report not found")
