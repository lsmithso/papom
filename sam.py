# Sound architecture models

import sys, os, dbus, logging

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

class Node(object):
    nodes = {}

    @classmethod
    def build(klass, conn, core, name):
	for path in  core.Get("org.PulseAudio.Core1", name, dbus_interface=I_PROP):
	    obj = conn.get_object(object_path = path)
	    klass.nodes[path] = klass(path, obj)
	
    def __init__(self, path, obj):
	self.path = path
	self.obj = obj



class ControlsMixin(object):

    I_DEVICE = "org.PulseAudio.Core1.Device"
    
    def get_volume(self):
	# Assumes balanced mono
	    vs = self.obj.Get(self.I_DEVICE, "Volume",  dbus_interface=I_PROP)
	    return  int(vs[0])
	    

    def set_volume(self, v):
	v1 = dbus.UInt32(v)
	self.obj.Set(self.I_DEVICE, "Volume", [v1, v1], dbus_interface = I_PROP)

    volume = property(get_volume, set_volume)

    def get_mute(self):
	return 	    self.obj.Get(self.I_DEVICE, "Mute",  dbus_interface=I_PROP)


    def set_mute(self, v):
	self.obj.Set(self.I_DEVICE, "Mute", v, dbus_interface=I_PROP)
	    
    mute = property(get_mute, set_mute)
    
	

class Sink(Node, ControlsMixin):

    I_SINK_PROP =  "org.PulseAudio.Core1.Device"

    @classmethod
    def build(klass, conn, core):
	super(Sink, klass).build(conn, core, 'Sinks')
	
    def __init__(self, path, obj):
	super(Sink, self).__init__(path, obj)
	self.index = self.obj.Get(self.I_SINK_PROP, "Index",  dbus_interface=I_PROP)	
	self.name = self.obj.Get(self.I_SINK_PROP, "Name", dbus_interface=I_PROP)
	

    def __str__(self):
	return 'Sink %d: %s %s %s' % (self.index, self.name, self.volume, self.mute)

class PlaybackStream(object):
    pass

class Client(object):
    pass



if __name__ == '__main__':
    # Self test
    logging.basicConfig(level=logging.DEBUG)                                                      
    conn, core = get_core()
    Sink.build(conn, core)
    for k, v in Sink.nodes.items():
	print k, v
	if v.index == 0:
	    print v.volume
	    v.volume = 60000
	    print v.mute
	    v.mute = False
