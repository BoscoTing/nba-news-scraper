from apscheduler.events import (
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    JobEvent,
)
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone

from app.core.logger import logger


def job_listener(event: JobEvent):
    if event.exception:
        logger.error(f"Job {event.job_id} failed: {event.exception}")

    elif event.code == EVENT_JOB_MISSED:
        logger.error(f"Job {event.job_id} missed its run time.")


async def log_scheduled_jobs():
    """Log all scheduled jobs with their next run time."""
    jobs = scheduler.get_jobs()
    if jobs:
        logger.info(f"Currently scheduled jobs ({len(jobs)}):")
        for job in jobs:
            next_run = job.next_run_time.strftime("%Y-%m-%d %H:%M:%S") if job.next_run_time else "Not scheduled"
            logger.info(f"Job ID: {job.id}, Next run: {next_run}")
    else:
        logger.info("No jobs currently scheduled.")


scheduler = BlockingScheduler(timezone=timezone("Asia/Taipei"))

scheduler.add_listener(
    job_listener,
    EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED
)

scheduler.add_job(
    log_scheduled_jobs,
    'interval',
    hours=1,
    id='log_scheduled_jobs',
    misfire_grace_time=10,
    coalesce=True,
    max_instances=1
)
