* Pulseaudio stfu

** Introduction
Acts on playback streams, selected by pid, process name, xid.
Nultiple streams may be selected by specifying pid lists, or with a process name that matches multiple processess.
Streams may be moved to a new sink
Streams may be muted
Streams may have volume set
Stream selection may be notted - acts on all but selected. ie mute all except Skype.

TODO:
Look at Xid
Look at process tree to find any parents or siblings that are sinks.

* Implementation
Classes for:
  Clients matched by pid, process name etc. class dict to match.
Device matched by name or submatch
  

class Sink:
   sinks = {}   Keyed by path

   @classnethod
    def load(conn):
   dbus calls to list + enuumerate sinks and add to static sinks

    @classnethod
   find((klass, path):
    return Sink from static
)



