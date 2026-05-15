import threading
import time
import schedule

class WorkflowEngine:
    """
    A simple background engine to run scheduled autonomous tasks or workflows.
    """
    def __init__(self):
        self._running = False
        self._thread = None

    def start(self):
        """Starts the workflow engine loop in a background daemon thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        print("🔁 Workflow Engine started.")

    def stop(self):
        """Stops the workflow engine loop."""
        self._running = False

    def _run_loop(self):
        """Internal loop executing scheduled tasks."""
        while self._running:
            schedule.run_pending()
            time.sleep(1)

    def register_daily_task(self, time_str: str, job_func, *args, **kwargs):
        """
        Registers a task to run daily at a specific time.

        Args:
            time_str: The time to run the task (e.g., '10:30').
            job_func: The function to execute.
        """
        schedule.every().day.at(time_str).do(job_func, *args, **kwargs)
        print(f"✅ Registered daily task at {time_str}")

    def register_interval_task(self, minutes: int, job_func, *args, **kwargs):
        """
        Registers a task to run every X minutes.

        Args:
            minutes: Interval in minutes.
            job_func: The function to execute.
        """
        schedule.every(minutes).minutes.do(job_func, *args, **kwargs)
        print(f"✅ Registered interval task every {minutes} minutes")

# Singleton instance to be used across the app
engine = WorkflowEngine()
engine.start()
