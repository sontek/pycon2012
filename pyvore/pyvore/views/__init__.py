from pyramid.view import view_config
from pyramid.response import Response

from pyvore.lib import get_session

from pyramid_socketio.io import SocketIOContext
from pyramid_socketio.io import socketio_manage

from json import dumps
from json import loads

import redis
import gevent

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
    jobs = []

    def listener(self, channel):
        r = redis.StrictRedis()
        r = r.pubsub()

        # only subscribe to the channel we are currently in
        r.subscribe('chat:' + channel)

        for m in r.listen():
            if not self.io.session.connected:
                return

            if m['type'] == 'message':
                data = loads(m['data'])
                self.io.send_event("chat", data)

    def event_subscribe(self, channel):
        result = self.spawn(self.listener, channel[0])
        self.jobs.append(result)

    def event_chat(self, msg):
        r = redis.Redis()
        # only publish to the channel the message came from
        r.publish('chat:' + msg[0], dumps(msg[1]))

@view_config(route_name='socket_io')
def socketio_service(request):
    retval = socketio_manage(ConnectIOContext(request))
    return Response(retval)
