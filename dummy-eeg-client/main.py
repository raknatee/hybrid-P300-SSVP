import asyncio
import websockets
import time
import json
import datetime
async def mock_eeg():
    async with websockets.connect("ws://ml-server:8000/eeg_streaming") as websocket:

        while True:
            await websocket.send(json.dumps({
                'timestamp':datetime.datetime.now().timestamp(),
                'data':
                [9.9]*8
            }))
            await asyncio.sleep(1)
     

# for i in range(5,0,-1):
#     print(f"mock eeg client will be ready in {i}")
#     time.sleep(1)

asyncio.run(mock_eeg())
 