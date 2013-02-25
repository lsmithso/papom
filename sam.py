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


class Sink(object):
    sinks = {}

    @classmethod
    def build(klass, conn, core):
	for path in  core.Get("org.PulseAudio.Core1", "Sinks", dbus_interface=I_PROP):
	    obj = conn.get_object(object_path = path)
	    klass.sinks[path] = klass(path, obj)
	
    def __init__(self, path, obj):
	self.path = path
	self.obj = obj
	self.index = self.obj.Get("org.PulseAudio.Core1.Device", "Index",  dbus_interface=I_PROP)	
	self.name = self.obj.Get("org.PulseAudio.Core1.Device", "Name", dbus_interface=I_PROP)
	
    def get_volume(self):
	pass

    def set_volume(self, v):
	pass

    def get_mute(self):
	pass

    def set_mute(self, v):
	pass

    def __str__(self):
	return '%d: %s' % (self.index, self.name)

class PlaybackStream(object):
    pass

class Client(object):
    pass



if __name__ == '__main__':
    # Self test
    logging.basicConfig(level=logging.DEBUG)                                                      
    conn, core = get_core()
    Sink.build(conn, core)
    for k, v in Sink.sinks.items():
	print k, v
    
    
    
