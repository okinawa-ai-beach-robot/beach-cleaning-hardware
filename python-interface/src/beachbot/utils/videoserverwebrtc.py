import cv2
from av import VideoFrame
from aiohttp import web
from aiortc import MediaStreamTrack
from aiortc import RTCPeerConnection, RTCSessionDescription
import datetime
import sys
import numpy as np
import asyncio


class VideoServerWebRTC(MediaStreamTrack):
    def __init__(self, fps=10, capture_width=1920, capture_height=1080,  port=5001) -> None:
        super().__init__()
        self.queue = asyncio.Queue(10)

        self.pcs = set()

        self.app = web.Application()
        self.app.on_shutdown.append(self.on_shutdown)
        self.app.router.add_get("/", self.index)
        self.app.router.add_post("/offer", self.offer)
        web.run_app(self.app, host="0.0.0.0", port=port)


    async def offer(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        pc = RTCPeerConnection()
        pcs.add(pc)

        # open media source
        video = self

        pc.addTrack(video)

        await pc.setRemoteDescription(offer)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )
    async def on_shutdown(self, app):
        coros = [pc.close() for pc in self.pcs]
        await asyncio.gather(*coros)
        self.pcs.clear()

    async def index(request):
        content = "test" #open(os.path.join(ROOT, "index.html"), "r").read()
        return web.Response(content_type="text/html", text=content)

    def add_frame(self, frame):
        try:
            self.queue.put_nowait(img)
        except asyncio.queues.QueueFull:
            pass
        _frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.vidserver.write(_frame)

    async def add_image_async(self, img: np.ndarray):
        await self.queue.put(img)
  
    async def recv(self):
        img = await self.queue.get()
        frame = VideoFrame.from_ndarray(img, format="bgr24")
        pts, time_base = await self.next_timestamp()
        frame.pts = pts
        frame.time_base = time_base
        return frame

    def close(self):
        pass




