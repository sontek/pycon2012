#!/usr/bin/env python
import sys

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid_socketio.io import SocketIOContext, socketio_manage

from socketio import SocketIOServer

import redis

def simple_route(config, name, url, fn):
    config.add_route(name, url)
    config.add_view(fn, route_name=name,
            renderer="example2:templates/%s.mako" % name)

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
                self.io.send_event("chat", m['data'])

    def connect(self):
        self.spawn(self.listener)

    def event_chat(self, msg):
        r = redis.Redis()
        r.publish('chat', msg[0])

def socketio_service(request):
    retval = socketio_manage(ConnectIOContext(request))
    return Response(retval)

def main(global_config, **settings):
    config = Configurator()

    simple_route(config, 'index', '/', index)
    simple_route(config, 'socket_io', 'socket.io/*remaining', socketio_service)

    config.add_static_view('static', 'static', cache_max_age=3600)

    app = config.make_wsgi_app()

    return app
