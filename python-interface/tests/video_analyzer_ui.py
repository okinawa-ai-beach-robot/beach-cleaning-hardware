#!/usr/bin/env python3
import base64
import signal
import time
from datetime import datetime

import cv2
import numpy as np
from fastapi import Response

from nicegui import Client, app, core, run, ui

# In case you don't have a webcam, this will provide a black placeholder image.
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')
# OpenCV is used to access the webcam.
video_capture = cv2.VideoCapture(0)




def convert(frame: np.ndarray) -> bytes:
    _, imencode_image = cv2.imencode('.jpg', frame)
    return imencode_image.tobytes()


@app.get('/video/frame')
# Thanks to FastAPI's `app.get`` it is easy to create a web route which always provides the latest image from OpenCV.
async def grab_video_frame() -> Response:
    if video_capture is None or not video_capture.isOpened():
        return placeholder
    # The `video_capture.read` call is a blocking function.
    # So we run it in a separate thread (default executor) to avoid blocking the event loop.
    _, frame = await run.io_bound(video_capture.read)
    if frame is None:
        return placeholder
    # `convert` is a CPU-intensive function, so we run it in a separate process to avoid blocking the event loop and GIL.
    jpeg = await run.cpu_bound(convert, frame)
    return Response(content=jpeg, media_type='image/jpeg')




async def disconnect() -> None:
    """Disconnect all clients from current running server."""
    for client_id in Client.instances:
        await core.sio.disconnect(client_id)


def handle_sigint(signum, frame) -> None:
    # `disconnect` is async, so it must be called from the event loop; we use `ui.timer` to do so.
    ui.timer(0.1, disconnect, once=True)
    # Delay the default handler to allow the disconnect to complete.
    ui.timer(1, lambda: signal.default_int_handler(signum, frame), once=True)


async def cleanup() -> None:
    # This prevents ugly stack traces when auto-reloading on code change,
    # because otherwise disconnected clients try to reconnect to the newly started server.
    await disconnect()
    # Release the webcam hardware so it can be used by other applications again.
    video_capture.release()

app.on_shutdown(cleanup)
# We also need to disconnect clients when the app is stopped with Ctrl+C,
# because otherwise they will keep requesting images which lead to unfinished subprocesses blocking the shutdown.
signal.signal(signal.SIGINT, handle_sigint)







dt = datetime.now()

async def handle_connection(cl : Client):
    global dt
    dt = datetime.now()
    await cl.connected()
    res = await cl.run_javascript("[window.screen.width,window.screen.height]")

    print(dt, res)
def handle_start():
    global dt
    dt = datetime.now()
    print(dt, "start")
app.on_connect(handle_connection)
app.on_startup(handle_start)

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='settings').props('flat color=white')
    ui.space()
    ui.button( icon='error').props('flat color=white')

with ui.footer(value=False) as footer:
    ui.label('Beachbot robot, OIST x Community, Onna-son, Okinawa')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Configure:')
    with ui.card().classes('w-full'):
        lbl1 = ui.label('System:')
        ui.button('Shut Down', on_click=lambda: ui.label('Please Wait'))
        ui.separator()
        ui.switch("1")
        ui.switch("2")
        ui.switch("3")
        #ui.timer(1.0, lambda: ui.label('Tick!'), once=True)


with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')


with ui.row().classes('w-full'):
    with ui.card().style('width: 45%'):
        ui.label('Video Analyzer:')
        image = ui.interactive_image(source="https://picsum.photos/id/684/640/360",size=(512,512)).style('width: 100%')
        slider = ui.slider(min=0, max=100, value=50)
        ui.label().bind_text_from(slider, 'value', backward=lambda a: f'Frame {a} of XX')
        def up_img(obj : ui.interactive_image, pleft=0, ptop=0, w=25, h=25):
            color = 'SkyBlue'
            color = '#FF0000' 
            obj.content = f'<rect x="{pleft}%" y="{ptop}%" ry="15" height="{h}%" width="{w}%" fill="none" stroke="{color}" stroke-width="4" />'
            obj.set_source(f'/video/frame?{time.time()}')

        ui.timer(1.0, lambda: up_img(image))

        

#ui.timer(interval=0.1, callback=lambda: video_image.set_source(f'/video/frame?{time.time()}'))

ui.run(title="Beachbot Video Analyzer", port=4321)
