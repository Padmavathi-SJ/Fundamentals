import time  # for time tracking

# store request timestamps per API key
buckets = {}

RATE_LIMIT = 5      # max 5 requests
TIME_WINDOW = 60    # per 60 seconds

def is_allowed(api_key):
    now = time.time()  # current time

    # create bucket if new user
    if api_key not in buckets:
        buckets[api_key] = []

    # remove old timestamps outside window
    buckets[api_key] = [
        t for t in buckets[api_key]
        if now - t < TIME_WINDOW
    ]

    # check limit
    if len(buckets[api_key]) >= RATE_LIMIT:
        return False  # limit exceeded

    # add current request
    buckets[api_key].append(now)

    return True  # allowed