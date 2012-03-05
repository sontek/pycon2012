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

def socketio_service(request):
    socketio = request.environ["socketio"]
    socketio.start_heartbeat()

    while True:
        message = socketio.receive()

        if message:
            print message["type"]
            if message["type"] == "message":
                socketio.broadcast_event("custom event", "omgz")
            elif message["type"] == "event":
                if message['name'] == "chat":
                    socketio.broadcast_event('chat', ''.join(message['args']))

    return {}

class ConnectIOContext(SocketIOContext):
    def connect(self):
        print 'CONNECTED!!'

    def disconnect(self):
        print 'disconnected!!'

    def event_chat(self, msg):
        print "MESSAGE!!!", msg
        self.broadcast_event("chat", msg)

def socketio_service2(request):
    print "Socket.IO request running"
    ctx = ConnectIOContext(request)
    retval = socketio_manage(ctx)
    return Response(retval)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass the port number ./app.py <port>")
    else:
        from gevent import monkey; monkey.patch_all()

        config = Configurator()

        simple_route(config, 'index', '/', index)
        #simple_route(config, 'socket_io', 'socket.io/*remaining', socketio_service)
        simple_route(config, 'socket_io', 'socket.io/*remaining', socketio_service2)

        config.add_static_view('static', 'static', cache_max_age=3600)

        app = config.make_wsgi_app()

        port = sys.argv[1]

        print("Listening on http://127.0.0.1:" + port)
        SocketIOServer(('127.0.0.1', int(port)), app, namespace="socket.io", policy_server=False).serve_forever()
