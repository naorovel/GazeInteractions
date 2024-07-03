from tobii_stream_engine import Api, Device, GazePoint, EyePosition, Stream, GazeOrigin, GazePoint, Stream, UserPresence, get_api_version
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

tobiiAPI = Api(); 

app = Flask("GazeInteractions")
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

gaze_point: GazePoint = None
gaze_origin: GazeOrigin = None
eye_position: EyePosition = None
user_presence: UserPresence = None
timestamp: int = 0

prev_data: dict = {
    "gaze_point": gaze_point,
    "gaze_origin": gaze_origin,
    "eye_position": eye_position,
    "user_presence": user_presence
}

@app.route('/')
def index():
  return render_template('index.html', async_mode=socketio.async_mode)

def emit_data(data: any):
    global prev_data
    prev_data.update(data)
    socketio.emit("update", data)
    print(prev_data)


def on_gaze_point(timestamp: int, gaze_point: GazePoint) -> None:
    emit_data({"gaze_point": gaze_point, "timestamp": timestamp})
    return gaze_point

def on_gaze_origin(timestamp: int, gaze_origin: GazeOrigin) -> None:
    emit_data({"gaze_origin": gaze_origin, "timestamp": timestamp})
    return gaze_origin

def on_eye_position(timestamp: int, eye_position: EyePosition) -> None:
    emit_data({"eye_position": eye_position, "timestamp": timestamp})
    return eye_position

def on_user_presence(timestamp: int, user_presence: UserPresence) -> None:
    emit_data({"user_presence": user_presence, "timestamp": timestamp})
    return user_presence

device_urls = tobiiAPI.enumerate_local_device_urls()

if not len(device_urls):
    print("no device found") 
    Exception(ValueError) # Change error type here to be more descriptive - no device found

device = Device(api=tobiiAPI, url=device_urls[0])
supported_capabilities = device.get_supported_capabilities()

supported_streams = device.get_supported_streams()

if Stream.GAZE_POINT in supported_streams:
    device.subscribe_gaze_point(callback=on_gaze_point)

if Stream.GAZE_ORIGIN in supported_streams:
    device.subscribe_gaze_origin(callback=on_gaze_origin)

if Stream.EYE_POSITION_NORMALIZED in supported_streams:
    device.subscribe_eye_position(callback=on_eye_position)

if Stream.USER_PRESENCE in supported_streams:
    device.subscribe_user_presence(callback=on_user_presence)

device.run()

if __name__ == "__main__":
    socketio.run(app, debug=True)
