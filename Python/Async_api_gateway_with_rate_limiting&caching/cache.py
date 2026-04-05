import time  # for TTL

cache_store = {}  # in-memory cache

def get_cache(key):
    if key in cache_store:
        value, expiry = cache_store[key]

        # check if still valid
        if time.time() < expiry:
            return value  # cache hit
        
        else:
            del cache_store[key]  # remove expired
    
    return None  # cache miss

def set_cache(key, value, ttl=30):
    expiry = time.time() + ttl # set expiry time
    cache_store[key] = (value, expiry)
