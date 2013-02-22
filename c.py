# user configured server start 
import dbus
import os
 
def connect():
    if 'PULSE_DBUS_SERVER' in os.environ:
        address = os.environ['PULSE_DBUS_SERVER']
    else:
        bus = dbus.SessionBus()
        server_lookup = bus.get_object("org.PulseAudio1", "/org/pulseaudio/server_lookup1")
        address = server_lookup.Get("org.PulseAudio.ServerLookup1", "Address", dbus_interface="org.freedesktop.DBus.Properties")

    return dbus.connection.Connection(address)

conn = connect()
core = conn.get_object(object_path="/org/pulseaudio/core1")
print "Successfully connected to " + core.Get("org.PulseAudio.Core1", "Name", dbus_interface="org.freedesktop.DBus.Properties") + "!"

print core.Get("org.PulseAudio.Core1", "Version", dbus_interface="org.freedesktop.DBus.Properties")

# get_object - returns proxy. Need dottted object name + / object path
# to work on. /SinkN is obbject path?
#Proxy calls need fn name, args, and bus_interface dotted arg.

for x in  core.Get("org.PulseAudio.Core1", "Sinks", dbus_interface="org.freedesktop.DBus.Properties"):
    s = conn.get_object(object_path = x)
    print s.Get("org.PulseAudio.Core1.Device", "Index",  dbus_interface="org.freedesktop.DBus.Properties")
    print s.Get("org.PulseAudio.Core1.Device", "Name",  dbus_interface="org.freedesktop.DBus.Properties")
    vs = s.Get("org.PulseAudio.Core1.Device", "Volume",  dbus_interface="org.freedesktop.DBus.Properties")
    print vs[0], vs[1]
    v1 = dbus.UInt32(vs[0] + 1000)
    #    s.Set("org.PulseAudio.Core1.Device", "Volume", [v1, v1],   dbus_interface="org.freedesktop.DBus.Properties" )
    

for x in  core.Get("org.PulseAudio.Core1", "Clients", dbus_interface="org.freedesktop.DBus.Properties"):
    print x
    s = conn.get_object(object_path = x)
    for k, v in   s.Get("org.PulseAudio.Core1.Client", "PropertyList",  dbus_interface="org.freedesktop.DBus.Properties", byte_arrays=True).items(): 
	print k, v
	
