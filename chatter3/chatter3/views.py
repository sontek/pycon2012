import redis
from json import loads
from json import dumps
import gevent

def index(request):
    """ Base view to load our template """
    return {}

def listener(io):
    """ Each client will spawn this listener thread to continually
    listen for publishes from redis
    """
    r = redis.StrictRedis()

    # enable redis pubsub ( new in 2.4 )
    r = r.pubsub()

    # subscribe to the chat channel
    r.subscribe('chat')

    for m in r.listen():
        # make sure the client hasn't disconnected
        if not io.session.connected:
            return

        if m['type'] == 'message':
            # load the json from redis and send it to the client
            data = loads(m['data'])
            io.send_event("chat", data)

def socketio_service(request):
    """ The view that will launch the socketio listener """
    r = redis.Redis()

    # gevent-socketio puts this into the environment
    socketio = request.environ["socketio"]

    # spawn the redis listener for the client
    gevent.spawn(listener, socketio)

    # keep trying to get messages from the websocket
    while True:
        message = socketio.receive()

        if message:
            if message["type"] == "event":
                if message['name'] == "chat":
                    # we got a new chat event from the client, send json encoded
                    # data to redis
                    r.publish('chat', dumps(message['args']))
    return {}
