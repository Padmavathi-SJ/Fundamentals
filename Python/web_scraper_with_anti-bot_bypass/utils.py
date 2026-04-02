from datetime import datetime
import time
import random

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def delay():
    time.sleep(random.uniform(1, 3))

    