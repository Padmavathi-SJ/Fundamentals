import time
# store failure count per service
# structure: { "user-service": 3, "order-service": 5}
failures = {}

# Track when each service last failed (for timeout calculation)
last_failed_time = {}

# circuit breaker config
MAX_FAILURES = 5  # Open circuit after 5 consecutive failures
RESET_TIMEOUT = 30 # Try again after 30 seconds

def is_open(service):
    """
    Check if circuit is open for a service.
    
    Circuit States:
     - Closed: Normal operation (requests go through)
     - Open: Too many failures (requests blocked)
     - Half-Open: After timeout, test if service recovered
    
    Returns:
        True: Circuit is OPEN - do not send requests
        False: Circuit is closed or half open - can send requests
    """
    # Get failure count for this service (default 0)
    if failures.get(service, 0) >= MAX_FAILURES:
        
        # check if enough time has passed to try again
        last_failed = last_failed_time.get(service, 0)
        time_since_failure = time.time() - last_failed

        if time_since_failure > RESET_TIMEOUT:
            # Timeout passed - transition to HALF-OPEN
            # Allow next request to test if service recovered
            return False  # half-open
        else:
            # Still within timeout - circuit remains OPEN
            return True
    # Less than MAX_FAILURES - circuit is CLOSED
    return False
  


def record_failure(service):
    # Record a failure for a service (increment counter)
    
    # increment failure count (default 0 if not exists)
    failures[service] = failures.get(service, 0) + 1

    # record timestamp of this failure
    last_failed_time[service] = time.time()


def reset(service):
    # Reset failure count after successful request (circuit closes)

    # reset to 0 failures
    failures[service] = 0