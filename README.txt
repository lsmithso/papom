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

Add pending ops on clients? Ie mute the next time it connects to a
stream? ie skype only sets up a playback stream in call, so cannot be
muted in advance. Needs sigmal signal to work.

Filter for loudest + quitest playback strams
rework filters to be non-generators. Static list that has no state.
sink name selector based on card/device/hw, rather tham pa name?
Play test sound.
Add move of sources. eg MIC to skype. This would allow ie files of credit card numbers etc tp be read out over the phone.
[OTT - add sound like notification ie cursor over mail, weather, irc status + beep]


CLI:
client: pname re|pexe re|pid. Can match multiple clients, sinks. !" negates inclusion. 
 mute !skype  - mutes all except skype
mute !skype  !sd-ibm  Mutes all except skype and ibm tts

pid can also match siblings + parent pids


sink = name re

beo
volume v [client|sink]
mute  [client|sink]
unmute   [client|sink]
 move client sink



