import time
import threading


class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time=30):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.last_failure_time = 0
        self.lock = threading.Lock()

    def is_open(self):
        with self.lock:
            if self.failures >= self.failure_threshold:
                if time.time() - self.last_failure_time < self.recovery_time:
                    return True
                else:
                    self.reset()

        return False

    def record_failure(self):
        with self.lock:
            self.failures += 1
            self.last_failure_time = time.time()

    def record_success(self):
        self.reset()

    def reset(self):
        with self.lock:
            self.failures = 0
            self.last_failure_time = 0
