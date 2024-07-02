import uvicorn
import json
import asyncio 
from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from tobii_stream_engine import Api, Device, GazePoint, EyePosition, Stream, GazeOrigin, GazePoint, Stream, UserPresence, get_api_version
from starlette.responses import StreamingResponse
from fastapi.testclient import TestClient

app = FastAPI()
tobiiAPI = Api(); 

def on_gaze_point(timestamp: int, gaze_point: GazePoint) -> None:
    # print(f"{gaze_point=}")
    return gaze_point

def on_gaze_origin(timestamp: int, gaze_origin: GazeOrigin) -> None:
    # print(f"{gaze_origin=}")
    return gaze_origin


def on_eye_position(timestamp: int, eye_position: EyePosition) -> None:
    # print(f"{eye_position=}")
    return eye_position


def on_user_presence(timestamp: int, user_presence: UserPresence) -> None:
    # print(f"{user_presence=}")
    return user_presence

@app.get("/")
async def root():
     return {"message": "hello world"}

@app.websocket("/datapoints")
async def datapoints(websocket: WebSocket):
    await websocket.accept()
    device_urls = tobiiAPI.enumerate_local_device_urls()

    if not len(device_urls):
    # print("no device found") 
        Exception(ValueError) # Change error type here to be more descriptive - no device found

    device = Device(api=tobiiAPI, url=device_urls[0])
    supported_capabilities = device.get_supported_capabilities()

    supported_streams = device.get_supported_streams()
    print(f"{supported_streams=}")

    if Stream.GAZE_POINT in supported_streams:
        gaze_point = device.subscribe_gaze_point(callback=on_gaze_point)

    if Stream.GAZE_ORIGIN in supported_streams:
        gaze_origin = device.subscribe_gaze_origin(callback=on_gaze_origin)

    if Stream.EYE_POSITION_NORMALIZED in supported_streams:
        eye_position = device.subscribe_eye_position(callback=on_eye_position)

    if Stream.USER_PRESENCE in supported_streams:
        user_presence = device.subscribe_user_presence(callback=on_user_presence)

    device.run()

    payload = {
        gaze_point: gaze_point,
        gaze_origin: gaze_origin,
        eye_position: eye_position, 
        user_presence: user_presence
    }

    await websocket.send_json(payload)
    await websocket.close()
    # test_websocket()

# test_websocket()