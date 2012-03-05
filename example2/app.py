#!/usr/bin/env python
import sys

from pyramid.config import Configurator
from socketio import SocketIOServer
from pyramid.response import Response
from pyramid_socketio.io import SocketIOContext, socketio_manage

def simple_route(config, name, url, fn):
    config.add_route(name, url)
    config.add_view(fn, route_name=name,
            renderer="__main__:templates/%s.mako" % name)

def index(request):
    return {}

class ConnectIOContext(SocketIOContext):
    def event_chat(self, msg):
        self.broadcast_event('chat', msg)

def socketio_service(request):
    print "Socket.IO request running"
    retval = socketio_manage(ConnectIOContext(request))
    return Response(retval)

if __name__ == '__main__':
    if len(sys.argv) < 1:
        port = int(sys.argv[1])
    else:
        port = 6543

    from gevent import monkey; monkey.patch_all()

    config = Configurator()

    simple_route(config, 'index', '/', index)
    simple_route(config, 'socket_io', 'socket.io/*remaining', socketio_service)

    config.add_static_view('static', 'static', cache_max_age=3600)

    app = config.make_wsgi_app()

    print("Listening on http://127.0.0.1:%s" % port)
    SocketIOServer(('127.0.0.1', port), app, namespace="socket.io", policy_server=False).serve_forever()
