import sys, os
import commands, sam


def usage():
    print 'Usage: stfu.py action args'
    print 'help, h, ? - print this message and exit'
    print 'print -- Print clients + sinks'
    print 'max -- set all streams + sinks to max volume & unmuted. Warning: will blow ears off'
    print 'volume [+-v] target -- set absolute volume, or incement/decrement current'
    print 'mute [target]'
    print 'unmute [target]'
    print 'move clients sink -- Move one or more clients to sink'
    sys.exit(1)

def resolve_client(arg):
    pass


def playback_streams(*args):
    rv = []
    for arg in args:
	for ps in arg.playback_links:
	    rv.append(ps)
    return rv

def resolve_targets(args):
    if not args:
	return commands.filter_all()
    rv = []
    for  arg in args:
	rv.append(commands.filter_sink(arg))
	cp = commands.filter_pid(arg)
	cn = commands.filter_process_name(arg)
	ce = commands.filter_exe_name(arg)
	rv.extend(playback_streams(cp, cn, ce))
    if not rc:
	usage()
    return set(rv)

def assert_int(v):
    try:
	return int(v)
    except ValueError, e:
	usage()
	
def main(args):
    if not args:
	usage()
	
    action = args[0]
    args= args[1:]
    debug= os.getenv('STFU_DEBUG')
    if debug and debug.lower() not in ('0', 'no', 'off'):
	logging.basicConfig(level=logging.DEBUG)
	
    sam.build_sam()

    if action in ('help', 'h', '?'):
	usage()
    elif action == 'print':
	commands.print_sam()
    elif action == 'max':
	commands.blow_ears_off()
    elif action == 'volume':
	if len(args) < 1:
	    usage()
	if args[0][0] in '+-':
	    v = assert_int(args[0][1:])
	    mpy = 1 if args[0][0] == '+' else -1
	    vfn = commands.incr_volume
	else:
	    v = assert_int(args[0])
	    mpy = 1
	    vfn = commands.set_volume
	targets = resolve_targets(args[1:])
	vfn(mpy * v, targets)
	print 'Set volume for target %s' % targets
    elif action == 'mute':
	pass
    elif action == 'unmute':
	pass
    elif  action == 'move':
	pass
    else:
	usage()
	
	
if __name__ == '__main__':
    main(sys.argv[1:])

    
