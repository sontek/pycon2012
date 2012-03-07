import redis
from json import loads
from json import dumps
import gevent

from chatter4.models import DBSession
from chatter4.models import Chat

def index(request):
    """ Base view to load our template """
    return {}

def get_log(request):
    return [c.serialize() for c in DBSession.query(Chat).all()]

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
                    chat_line = ''.join(message['args'])
                    chat = Chat(chat_line = chat_line)
                    DBSession.add(chat)
                    DBSession.commit()

                    # we got a new chat event from the client, send it out to
                    # all the listeners
                    r.publish('chat', dumps(chat.serialize()))
    return {}

