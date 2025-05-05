# X_Vector_Pro/engine/threading_manager.py

import threading
import queue
import time
from utils.logger import log_to_central

class ThreadingManager:
    def __init__(self, max_threads=10):
        self.max_threads = max_threads
        self.thread_queue = queue.Queue()
        self.running_threads = set()
        self.lock = threading.Lock()

    def _worker(self):
        while True:
            task = self.thread_queue.get()
            if task is None:  # No more tasks, exit thread
                break
            task_name, target, callback = task
            try:
                callback(target)
                log_to_central(f"[+] Task '{task_name}' executed on {target}")
            except Exception as e:
                log_to_central(f"[-] Task '{task_name}' failed on {target}: {e}")
            self.thread_queue.task_done()

    def add_task(self, task_name, target, callback):
        """Add a task to the queue to be processed by the worker threads."""
        self.thread_queue.put((task_name, target, callback))

    def start(self):
        """Start worker threads up to the max_thread limit."""
        for _ in range(self.max_threads):
            thread = threading.Thread(target=self._worker, daemon=True)
            thread.start()
            self.running_threads.add(thread)

    def stop(self):
        """Stop all worker threads."""
        for _ in range(self.max_threads):
            self.thread_queue.put(None)  # Stop signal for each worker thread
        for thread in self.running_threads:
            thread.join()

    def wait_for_completion(self):
        """Wait for all tasks in the queue to be completed."""
        self.thread_queue.join()

    def execute_tasks(self, tasks):
        """Execute a batch of tasks."""
        self.start()
        for task in tasks:
            task_name, target, callback = task
            self.add_task(task_name, target, callback)
        self.wait_for_completion()
        self.stop()

# Example usage in the X-Vector Pro
if __name__ == "__main__":
    threading_manager = ThreadingManager(max_threads=5)

    # Dummy function for simulating task execution
    def dummy_task(target):
        time.sleep(1)
        print(f"Executed task for {target}")

    # Tasks to be added
    tasks = [
        ("Exploit 1", "192.168.1.1", dummy_task),
        ("Exploit 2", "192.168.1.2", dummy_task),
        ("Exploit 3", "192.168.1.3", dummy_task),
    ]

    threading_manager.execute_tasks(tasks)
