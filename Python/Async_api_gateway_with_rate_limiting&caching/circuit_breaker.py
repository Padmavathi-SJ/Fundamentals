import time
# store failure count per service
failures = {}
last_failed_time = {}

# config
MAX_FAILURES = 5  # after 3 failures → circuit opens
RESET_TIMEOUT = 30 # seconds

def is_open(service):
    if failures.get(service, 0) >= MAX_FAILURES:
        # allow retry after timeout
        if time.time() - last_failed_time.get(service, 0) > RESET_TIMEOUT:
            return False  # half-open
        return True
    return False
  


def record_failure(service):
    # increase failure count
    failures[service] = failures.get(service, 0) + 1
    last_failed_time[service] = time.time()


def reset(service):
    # reset failure count after success
    failures[service] = 0