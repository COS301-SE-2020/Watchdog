import asyncio
import platform

from . import config
import socketio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer

conf = config.configure()
CLIENT_KEY = conf['services']['client']['key']
URL = conf['services']['stream_url']
FPS = conf['video']['frames_per_second']


class RTCConnectionHandler:
    def __init__(self, camera_id, user_id, camera_address):
        self.pc = {}
        self.pcs = set()
        self.socket = socketio.AsyncClient(ssl_verify=False)
        self.user_id = user_id
        self.camera_id = camera_id
        self.camera_address = camera_address

    async def start(self):
        status = False
        retry = 5
        # TODO: Make this exponential backoff time calculator
        calculate_time = lambda attempt: 5
        while not status and retry > 0:
            await self.socket.sleep(calculate_time(retry))
            try:
                await self.socket.connect(URL)
                status = True
            except Exception as e:
                print('Socket connection error...retrying')

        if retry == 0:
            print('Failed to connect')

        await self.register()
        await self.make_view_available()
        # while True:
        #     await self.socket.sleep(1)
        # await self.socket.wait()

        @self.socket.on('offer')
        async def process_offer(params):
            if params['camera_id'] != self.camera_id:
                return
            print('RECEIVED OFFER...')
            # params = await request.json()
            offer = RTCSessionDescription(sdp=params['offer']["sdp"], type=params['offer']["type"])

            pc = RTCPeerConnection()
            self.pc[params['camera_id']] = pc
            self.pcs.add(self.pc[params['camera_id']])

            @pc.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                print("ICE connection state is %s" % pc.iceConnectionState)
                if pc.iceConnectionState == "failed":
                    await pc.close()
                    self.pcs.discard(pc)

            # open media source
            options = {"framerate": "30"}
            print(f'fetching stream: {self.camera_address}')
            player = None
            if self.camera_address == '://0':
                if platform.system() == 'Darwin':
                    # Open webcam on OS X.
                    player = MediaPlayer('default:none', format='avfoundation', options={'framerate': '30'})
                else:
                    player = MediaPlayer('/dev/video0', format='v4l2')

            else:
                player = MediaPlayer(self.camera_address) # , options=options)
            # else:
            #     player = MediaPlayer("/dev/video0", format="v4l2", options=options)

            await pc.setRemoteDescription(offer)
            for t in pc.getTransceivers():
                if t.kind == "audio" and player.audio:
                    pc.addTrack(player.audio)
                elif t.kind == "video" and player.video:
                    pc.addTrack(player.video)

            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)

            # return web.Response(
            #     content_type="application/json",
            #     text=json.dumps(
            #         {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            #     ),
            # )
            print('SENDING ANSWER...')
            await self.socket.emit('answer', {
                'camera_id': params['camera_id'],
                'token': params['token'],
                'answer': {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            })

        @self.socket.on('registered')
        async def registered(data):
            print(data)

        @self.socket.on('disconnect')
        async def on_shutdown():
            # close peer connections
            print(f'disconnecting {self.camera_id}')
            coros = [pc.close() for pc in self.pcs]
            await asyncio.gather(*coros)
            self.pcs.clear()

        await self.socket.wait()

    async def register(self):
        print(f'Registering: {self.user_id}')
        await self.socket.emit('register', {
            'user_id': self.user_id,
            'client_type': 'producer',
            'data': {}
        })

    async def make_view_available(self):
        print(f'Making view Available: {self.camera_id}')
        await self.socket.emit('make-available', {
            'camera_id': self.camera_id,
            'camera': {}
        })
