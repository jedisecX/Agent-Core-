# app/tasks/queue.py

from datetime import datetime
import uuid


class TaskQueue:
    """
    Lightweight internal task queue

    Responsibilities:
    - persist deferred work
    - track execution status
    - prepare future autonomous scheduling
    - provide upgrade path to Redis/Celery later

    Current mode:
    in-memory queue
    """

    def __init__(self):
        self.tasks = []

    def create_task(
        self,
        task_type: str,
        payload: dict,
        priority: str = "normal"
    ) -> dict:
        """
        Add new queued task
        """

        task = {
            "task_id": str(uuid.uuid4()),
            "task_type": task_type,
            "payload": payload,
            "priority": priority,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        self.tasks.append(task)

        return task

    def get_all_tasks(self) -> list:
        """
        Return full task list
        """

        return self.tasks

    def get_task(
        self,
        task_id: str
    ) -> dict:
        """
        Retrieve single task
        """

        for task in self.tasks:
            if task["task_id"] == task_id:
                return task

        return {}

    def update_status(
        self,
        task_id: str,
        new_status: str
    ) -> bool:
        """
        Update task execution state
        """

        for task in self.tasks:
            if task["task_id"] == task_id:
                task["status"] = new_status
                task["updated_at"] = (
                    datetime.utcnow().isoformat()
                )
                return True

        return False

    def delete_task(
        self,
        task_id: str
    ) -> bool:
        """
        Remove completed or invalid task
        """

        for index, task in enumerate(self.tasks):
            if task["task_id"] == task_id:
                del self.tasks[index]
                return True

        return False


task_queue = TaskQueue()
