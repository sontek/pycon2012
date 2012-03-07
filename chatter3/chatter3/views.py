import redis
from json import loads
from json import dumps
import gevent

def index(request):
    """ Base view to load our template """
    return {}

def listener(io):
    r = redis.StrictRedis()
    r = r.pubsub()

    # only subscribe to the channel we are currently in
    r.subscribe('chat')

    for m in r.listen():
        if not io.session.connected:
            return

        if m['type'] == 'message':
            data = loads(m['data'])
            io.send_event("chat", data)

def socketio_service(request):
    """ The view that will launch the socketio listener """
    r = redis.Redis()

    # gevent-socketio puts this into the environment
    socketio = request.environ["socketio"]

    gevent.spawn(listener, socketio)

    # keep trying to get messages from the websocket
    while True:
        message = socketio.receive()

        if message:
            if message["type"] == "event":
                if message['name'] == "chat":
                    # we got a new chat event from the client, send it out to
                    # all the listeners
                    r.publish('chat', dumps(message['args']))
    return {}

