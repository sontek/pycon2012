def index(request):
    """ Base view to load our template """
    return {}

def socketio_service(request):
    """ The view that will launch the socketio listener """

    # gevent-socketio puts this into the environment
    socketio = request.environ["socketio"]

    # keep trying to get messages from the websocket
    while True:
        message = socketio.receive()

        if message:
            if message["type"] == "event":
                if message['name'] == "chat":
                    # we got a new chat event from the client, send it out to
                    # all the clients except ourselves
                    socketio.broadcast_event('chat', ''.join(message['args']))
    return {}

