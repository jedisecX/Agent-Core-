# app/tasks/scheduler.py

import time
from threading import Thread

from app.tasks.queue import task_queue


class TaskScheduler:
    """
    Lightweight autonomous scheduler

    Responsibilities:
    - poll queued tasks
    - trigger deferred execution
    - prepare upgrade path for Celery / Redis / distributed workers

    Current mode:
    background thread polling
    """

    def __init__(self):
        self.running = False
        self.poll_interval = 5  # seconds

    def start(self):
        """
        Start scheduler thread
        """

        if self.running:
            return

        self.running = True

        worker = Thread(
            target=self._scheduler_loop,
            daemon=True
        )

        worker.start()

        print("Task scheduler started.")

    def stop(self):
        """
        Stop scheduler
        """

        self.running = False
        print("Task scheduler stopped.")

    def _scheduler_loop(self):
        """
        Main background loop
        """

        while self.running:
            try:
                self._process_tasks()
            except Exception as e:
                print(
                    f"Scheduler execution error: {str(e)}"
                )

            time.sleep(self.poll_interval)

    def _process_tasks(self):
        """
        Execute queued tasks

        Current behavior:
        mark queued tasks as completed

        Next upgrade:
        real autonomous execution hooks
        """

        tasks = task_queue.get_all_tasks()

        for task in tasks:
            if task["status"] != "queued":
                continue

            print(
                f"Processing task: "
                f"{task['task_id']} "
                f"({task['task_type']})"
            )

            # Placeholder execution layer
            # Later:
            # route task into actual agent execution

            task_queue.update_status(
                task["task_id"],
                "completed"
            )


scheduler = TaskScheduler()
