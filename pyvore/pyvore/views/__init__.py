from pyramid.view import view_config
from pyramid.response import Response

from pyvore.lib import get_session

from pyramid_socketio.io import SocketIOContext
from pyramid_socketio.io import socketio_manage

from json import dumps
from json import loads

import redis

class BaseController(object):
    @property
    def request(self):
        # we defined this so that we can override the request in tests easily
        return self._request

    def __init__(self, request):
        self._request  = request

        self.settings = request.registry.settings
        self.db = get_session(request)

@view_config(route_name='index', renderer='base.jinja2')
def index(request):
    return {}

class ConnectIOContext(SocketIOContext):
    def listener(self):
        r = redis.Redis()
        r.subscribe('chat')

        for m in r.listen():
            if not self.io.session.connected:
                return

            if m['type'] == 'message':
                data = loads(m['data'])
                self.io.send_event("chat", data[1])

    def connect(self):
        print("CONNECT!!!")
        self.spawn(self.listener)

    def event_chat(self, msg):
        r = redis.Redis()
        r.publish('chat', dumps(msg))

@view_config(route_name='socket_io')
def socketio_service(request):
    print("SERVICE!!!")
    retval = socketio_manage(ConnectIOContext(request))
    return Response(retval)
