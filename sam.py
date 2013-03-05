# Sound architecture models

# TODO:
# Add print of client -> sink
# Handle race where nodes in the pa server are dleted while running
# Add move sink input
# improve __str__ format. L
# Only print last part of paths. Add src/sink to stream
#
import sys, os, dbus, logging, subprocess

logger = logging.getLogger(__name__)

I_PROP = "org.freedesktop.DBus.Properties"

def get_core():
    if 'PULSE_DBUS_SERVER' in os.environ:
        address = os.environ['PULSE_DBUS_SERVER']
    else:
        bus = dbus.SessionBus()
        server_lookup = bus.get_object("org.PulseAudio1", "/org/pulseaudio/server_lookup1")
        address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address", dbus_interface=I_PROP)

    conn = dbus.connection.Connection(address)
    logger.debug('connected to %s#', address)
    core = conn.get_object(object_path="/org/pulseaudio/core1")
    return conn, core

class NodeMeta(type):
    def __new__(meta, name, bases, dct):
	dct['nodes'] = {}
        return super(NodeMeta, meta).__new__(meta, name, bases, dct)

class Node(object):
    __metaclass__ = NodeMeta

    @classmethod
    def build(klass, conn, core, name):
	for path in  core.Get("org.PulseAudio.Core1", name, dbus_interface=I_PROP):
	    obj = conn.get_object(object_path = path)
	    klass.nodes[path] = klass(path, obj)
	
    def __init__(self, path, obj):
	self.path = path
	self.obj = obj

    @classmethod
    def make_links(klass):
	for node in klass.nodes.values():
	    node._make_links()


class ControlsMixin(object):

    
    def get_volume(self):
	# Assumes balanced mono
	    vs = self.obj.Get(self.I_CONTROL, "Volume",  dbus_interface=I_PROP)
	    return  int(vs[0])
	    

    def set_volume(self, v):
	v1 = dbus.UInt32(v)
	# Some streams/sinks are mono, and pa barfs if setting these
	# to more than one channel.
	vs = self.obj.Get(self.I_CONTROL, "Volume",  dbus_interface=I_PROP)
	self.obj.Set(self.I_CONTROL, "Volume", [v1] * len(vs), dbus_interface = I_PROP)
    volume = property(get_volume, set_volume)

    def get_mute(self):
	return 	    self.obj.Get(self.I_CONTROL, "Mute",  dbus_interface=I_PROP)


    def set_mute(self, v):
	self.obj.Set(self.I_CONTROL, "Mute", v, dbus_interface=I_PROP)
    mute = property(get_mute, set_mute)
    
	

class Sink(Node, ControlsMixin):

    I_SINK_PROP =  "org.PulseAudio.Core1.Device"
    I_CONTROL = I_SINK_PROP
    I_CONTROL = I_SINK_PROP
	
    @classmethod
    def build(klass, conn, core):
	super(Sink, klass).build(conn, core, 'Sinks')
	
    def __init__(self, path, obj):
	super(Sink, self).__init__(path, obj)
	self.index = self.obj.Get(self.I_SINK_PROP, "Index",  dbus_interface=I_PROP)	
	self.name = self.obj.Get(self.I_SINK_PROP, "Name", dbus_interface=I_PROP)
	self.playback_links = []
	logger.debug('Added: %s', self)
	

    def _make_links(self):
	# Sinks don't have a path back to Playback Streams, so artifice one.
	for ps  in PlaybackStream.nodes.values():
	    if ps.sink_link == self:
		self.playback_links.append(ps)
    def __str__(self):
	return 'Sink %d: %s %s %s' % (self.index, self.name, self.volume, self.mute)


class PlaybackStream(Node, ControlsMixin):
    I_STREAM_PROP =  "org.PulseAudio.Core1.Stream"
    I_CONTROL = I_STREAM_PROP

    @classmethod
    def build(klass, conn, core):
 	super(PlaybackStream, klass).build(conn, core, 'PlaybackStreams')
	
    def __init__(self, path, obj):
	super(PlaybackStream, self).__init__(path, obj)
	self.index = self.obj.Get(self.I_STREAM_PROP, "Index", dbus_interface=I_PROP)
	self.client_path = self.obj.Get(self.I_STREAM_PROP, "Client", dbus_interface=I_PROP)
	self.sink_path = self.obj.Get(self.I_STREAM_PROP, "Device", dbus_interface=I_PROP)
	logger.debug('Added: %s', self)

    def _make_links(self):
	self.sink_link = Sink.nodes[self.sink_path]
	self.client_link = Client.nodes[self.client_path]

	
    def move(self, sink):
	logger.debug('moving %s to %s', self, sink.path)
	if 0:
	    # pulseaudio dbus i/f asserts . POS.
	    self.obj.Move(sink.path, dbus_interface = 'org.PulseAudio.Core1.Stream')
	else:
	    # Workround - spawn pacmd.
	    cmd = 'pacmd move-sink-input %d %d' % (self.index, sink.index)
	    logger.debug('pa move bug cmd: %s', cmd)
	    pipe = subprocess.Popen(cmd.split(), stdin=None, stdout=subprocess.PIPE,
				    stderr=sys.stderr)
	    rsp = pipe.stdout
	    logger.debug('pacmd rsp: %s', rsp.read(4*1024))
	

    def __str__(self):
	return 'Playback %d: %s (%s) %s' % (self.index,self.client_link,  self.volume, self.mute)



class Client(Node):

    I_CLIENT_PROP =  "org.PulseAudio.Core1.Client"

    @classmethod
    def build(klass, conn, core):
 	super(Client, klass).build(conn, core, 'Clients')
	
    def __init__(self, path, obj):
	super(Client, self).__init__(path, obj)
	self.playback_links = []
	self.index = self.obj.Get(self.I_CLIENT_PROP, "Index", dbus_interface=I_PROP)
	self.playback_streams = self.obj.Get(self.I_CLIENT_PROP, "PlaybackStreams", dbus_interface=I_PROP)
	prop_list = self.obj.Get(self.I_CLIENT_PROP, "PropertyList",  dbus_interface=I_PROP, byte_arrays=True)

	# dbus returns byte array strings with a C style trailing null
	def get(n):
	    v = prop_list.get(n)
	    if v is not None:
		return str(v[:-1] if v[-1] == '\x00' else v)
	
	self.a_name = get('application.name')
	v = get('application.process.id')
	self.a_pid = int(v) if v else 0
	self.a_exe = get('application.process.binary')
	logger.debug('Added: %s', self)
	

    def _make_links(self):
	# Dunno why streams links are arrays
	for ps in self.playback_streams:
	    self.playback_links.append(PlaybackStream.nodes[ps])

    
    def __str__(self):
	return 'Client %d: %s %s %s' % (self.index, self.a_name, self.a_exe, self.a_pid)




def build_sam():
    conn, core = get_core()
    Sink.build(conn, core)
    PlaybackStream.build(conn, core)
    Client.build(conn, core)
    Client.make_links()
    PlaybackStream.make_links()
    Sink.make_links()
    

if __name__ == '__main__':
    # Self test
    logging.basicConfig(level=logging.DEBUG)
    build_sam()
    print '*** Sinks', id(Sink.nodes)
    for k, v in Sink.nodes.items():
	print k, v
	if v.index == 0:
	    print v.volume
	    v.volume = 60000
	    print v.mute
	    v.mute = False

    print '*** Streams', id(PlaybackStream.nodes)
    for k, v in PlaybackStream.nodes.items():
	print k, v
	if 0 and v.index == int(sys.argv[1]):
	    v.mute = False
    print '*** Clients'
    for k, v in Client.nodes.items():
	print k, v
	print '|'.join([str(x) for x in v.playback_links])
    
