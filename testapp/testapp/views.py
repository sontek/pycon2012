from pyramid.view import view_config
import gevent
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin

def index(request):
    """ Base view to load our template """
    return {}


class GlobalIONamespace(BaseNamespace, BroadcastMixin):
    def on_chat(self, *args):
        self.emit("bob", {'hello': 'world'})
    
    def recv_connect(self):
        self.emit("you_just_connected", {'bravo': 'kid'})
        self.spawn(self.cpu_checker_process)

    def on_bob(self, *args):
        self.broadcast_event('broadcasted', args)
        self.socket['/chat'].emit('bob')

    def cpu_checker_process(self):
        """This will be a greenlet"""
        ret = os.system("cat /proc/cpu/stuff")
        self.emit("cpu_value", ret)

class ChatIONamespace(BaseNamespace, RoomsMixin):
    def on_mymessage(self, msg):
        print "In on_mymessage"
        self.send("little message back")
        self.send({'blah': 'blah'}, json=True)
        for x in xrange(100):
            self.emit("pack", {'the': 'more', 'you': 'can'})

nsmap = {'': GlobalIONamespace,
         '/chat': ChatIONamespace}

@view_config(route_name='socket_io')
def socketio_service(request):
    """ The view that will launch the socketio listener """

    socketio_manage(request.environ, namespaces=nsmap, request=request)

    return {}

