from __future__ import annotations

from arq import Worker


class WorkerSettings:
    cron_jobs = []
    queue_name = "speaking-coach"

    @classmethod
    def get_jobs(cls):
        return []


async def process_recording_job(ctx, recording_id: str) -> dict:
    return {"recording_id": recording_id, "status": "queued"}


async def main() -> Worker:
    return Worker(asyncio_tasks=[process_recording_job], cron_jobs=[], queue_name="speaking-coach")
