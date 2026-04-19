from fastapi import FastAPI, WebSocket  # FastAPI framework and WebSocket support
from fastapi.responses import HTMLResponse # For serving HTML pages
from contextlib import asynccontextmanager  # NEW: Import for lifespan management
import asyncio # For async operations and background tasks 
from datetime import datetime

from sensor import sensor_stream # importing the simulated sensor data generator
from processor import process # Importing the data processing functions

# store connected websocket clients in a list
# Each client is a websocket connection from a browser
connected_clients = [] 

# LIFESPAN CONTEXT MANAGER (replaces @app.on_event)
# this manages what happens when the server starts and stops
# code before 'yield' runs at startup
# code after 'yeild' runs at shutdown

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages startup and shutdown events.
    Code before yield runs at startup.
    Code after yield runs at shutdown.
    """
    # --- STARTUP (runs once when server starts) ---
    print("[INFO] Stream processor started — consuming from sensors/factory-a")
    print("[INFO] Dashboard available at http://localhost:8000/")
    
    # Start the background streaming task
    # asyncio.create_task() runs a coroutine in the background
    # This task will continuously read sensor data and broadcast to clients
    task = asyncio.create_task(broadcast_sensor_data())
    
    # Yield control to the application -it gives control to FastAPI
    # FastAPI runs the application while function is paused at yield
    yield
    
    # --- SHUTDOWN (runs when server stops) ---
    print("[INFO] Shutting down...")
    task.cancel()  # Stop the streaming task
    await task  # Wait for it to finish
    print("[INFO] Stream processor stopped")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)


# Serve Dashboard HTML
# @app.get decorator maps the HTTP GET requests to this function
@app.get("/")
async def get_dashboard():
    """Serve the dashboard HTML page"""
    # with statement automatically closes the file when done
    with open("templates/dashboard.html", "r") as f:
        # Read the entire file content and return as HTML response
        return HTMLResponse(f.read())


# WebSocket Connection endpoint
# websockets are persistent, two-way connections
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    print(f"[INFO] {len(connected_clients)} client(s) connected")
    
    try:
        # Keep connection alive
        while True:
            await asyncio.sleep(1)
    except:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        print(f"[INFO] Client disconnected ({len(connected_clients)} remaining)")


async def broadcast_sensor_data():
    # Main loop: get data from sensor, process it, send to the all connected clients.
    # this runs continuously in the background as long as the server is running.
    
    print("\n=== Live sensor Feed (every 1s) ===")

    # Iterate over the async generator - gets one reading per second
    # 'async for' is used with async generators (can pause between itrations)
    async for sensor_data in sensor_stream():

        # process the raw sensor data (calculate moving avg, standard deviation, z-score)
        processed = process(sensor_data)

        # Get timestamp
        now = datetime.now().strftime("%H:%M:%S")

        # print to console
        print(f"[{now} sensor--{sensor_data['sensor']}  "
              f"temp={sensor_data['temperature']}F  "
              f"vibration={sensor_data['vibration']}g  "
              f"status={processed['status']}")
        
        # Trigger alert for critical
        if processed["status"] == "CRITICAL":
            print(f"\n=== Alert Triggered ===")
            print(f"[ALERT] sensor-{sensor_data['sensor']} - Temperature exceeded threshold (>100F)")
            print(f"Current: {sensor_data['temperature']}F | "
                  f"5-min avg: {processed['avg']}F | "
                  f"Deviation: +{processed['z']} sigma")
            print(f"Action:  Notification sent to ops-team@factory.com\n")


        # Merge raw and processed data for clients
        output = {
            "sensor": sensor_data["sensor"],
            "temperature": sensor_data["temperature"],
            "vibration": sensor_data["vibration"],
            "avg": processed["avg"],
            "z": processed["z"],
            "status": processed["status"]
        }


        # send to all connected clients
        for client in connected_clients[:]: # copy list to avoid modification issues
            try:
                await client.send_json(output)
            except:
                if client in connected_clients:
                    connected_clients.remove(client)
        
        # wait 1 second before next reading
        # this controls the data rate (1 reading per second)
        await asyncio.sleep(1)
                           

   