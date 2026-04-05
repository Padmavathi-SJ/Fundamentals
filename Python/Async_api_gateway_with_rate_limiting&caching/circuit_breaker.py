# store failure count per service
failures = {}

# config
MAX_FAILURES = 3  # after 3 failures → circuit opens


def is_open(service):
    # return True if failure count exceeded
    return failures.get(service, 0) >= MAX_FAILURES


def record_failure(service):
    # increase failure count
    failures[service] = failures.get(service, 0) + 1


def reset(service):
    # reset failure count after success
    failures[service] = 0