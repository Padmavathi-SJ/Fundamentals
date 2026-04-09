import time  # for TTL

cache_store = {}  # in-memory cache

def get_cache(key):
    if key in cache_store:
        value, expiry = cache_store[key]

        remaining = expiry - time.time()

        if remaining > 0:
            return value, round(remaining)
        else:
            del cache_store[key]
    
    return None, 0  # cache miss

def set_cache(key, value, ttl=30):
    expiry = time.time() + ttl # set expiry time
    cache_store[key] = (value, expiry)
