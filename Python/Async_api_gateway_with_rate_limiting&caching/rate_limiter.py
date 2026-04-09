import time

buckets = {}

RATE = 10       # allow 10 requests
WINDOW = 60     # per 60 seconds

def is_allowed(api_key):
    now = time.time()

    # create bucket if not exists
    if api_key not in buckets:
        buckets[api_key] = {
            "tokens": RATE,
            "last": now
        }

    bucket = buckets[api_key]

    # refill tokens based on elapsed time
    elapsed = now - bucket["last"]
    refill = (elapsed / WINDOW) * RATE

    bucket["tokens"] = min(RATE, bucket["tokens"] + refill)
    bucket["last"] = now

    # check availability
    if bucket["tokens"] < 1:
        return False

    # consume token
    bucket["tokens"] -= 1
    return True