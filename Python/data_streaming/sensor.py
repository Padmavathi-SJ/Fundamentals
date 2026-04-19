import random # for generating random sensor readings
import asyncio # allows asynchronous operations (non-blocking delays)

# async generator function -> produces data continously
async def sensor_stream():
    """
    Async generator that produces simulated sensor data.
    Can be extended to support multiple sensors.

    This simulates a real IoT device sending data every second. 
    ex: A temperature sensor in a factory that sends readings every second 
    to a central monitoring system.
    """
   # Track how many readings we've sent
    reading_count=0

    # infinite loop - generator runs forever until stopped 
    # each iteration produces one sensor reading
    while True: 
        reading_count += 1 
         
        # create pattern to trigger alerts at regular intervals
        # every 15-29 readings, create a critical reading
        if reading_count % 15 == 0:
            # SPIKE - This will trigger CRITICAL
            temperature = random.uniform(102, 110) # Above 100 degree F

        # every 8th reading (8,16,24,32, ..) create warning
        # this will trigger warning alert  
        elif reading_count % 8 == 0:
            # WARN - This will trigger WARNING
            temperature = random.uniform(86, 99)  # above 85 degree F
           
        else:
            # NORMAL - Normal operation
            # random between 65 and 84 degree F (normal operating range)
            temperature = random.uniform(65, 84)  # Normal range
          
        # create the data dictionary (one complete sensor reading)
        data = {
            "sensor": "T1", # sensor ID (T1 - Temperature sensor 1)
            "temperature": round(temperature, 2), # Temperature in Fahrenheit (2 decimal places)
            "vibration": round(random.uniform(0.1, 0.6), 2) # Vibration in G-force
          
        }

        # yield sends the data to the caller, then pauses the generator
        # unlike return, yeild does not= end the function - it can resume later
        yield data

        # await asyncio.sleep(1) pauses execution for 1 second without blocking
        # this simulates real sensor reading intervals (1 reading per second)
        # the 'await' keyword is used with async functions to wait without blocking
       
        await asyncio.sleep(1)  # Send every second
