import sys, os
import commands, sam


def usage():
    print 'Usage: stfu.py action args'
    print 'help, h, ? - print this message and exit'
    print 'print -- Print clients + sinks'
    print 'max -- set all streams + sinks to max volume & unmuted. Warning: will blow ears off'
    print 'volume [+-] target -- set absolute volume, or incement/decrement current'
    print 'mute [target]'
    print 'unmute [target]'
    print 'move clients sink -- Move one or more clients to sink'
    sys.exit(1)

def resolve_client(arg):
    pass

def resolve_target(arg):
    pass

    
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
	pass
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

    
