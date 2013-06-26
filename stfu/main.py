# FIXME:
# RecordStream missing Volume attr.
# Add play: rec: to dst to disambiguate
# Test move

import sys, os, logging

import  commands,  sam

logger = logging.getLogger(__name__)

ARG_INVERT = '~'



def usage():
    print 'Usage: stfu.py action args'
    print 'help, h, ? - print this message and exit'
    print 'print -- Print sinks + sources + clients'
    print 'max -- set all streams + sinks + sources to max volume & unmuted. Warning: will blow ears off'
    print 'volume [+-v] target -- set absolute volume, or incement/decrement current'
    print 'mute [target]'
    print 'unmute [target]'
    print 'move sink clients  -- Move one or more clients to sink'
    print 'default_sink sink  -- set default sink to sink'
    print 'default_source source -- set default source to source'
    sys.exit(1)



def playback_streams(*args):
    rv = []
    for nodes in args:
	for node in nodes:
	    rv.extend(node.playback_links)
    return rv

def resolve_targets(args, pps = None):
    if not args:
	# FIXME: Should filter parent procs?
	return  commands.filter_controllable()
    rv = []
    for  arg in args:
	if arg[0] == ARG_INVERT:
	    invert = True
	    arg = arg[1:]
	else:
	    invert = False
	# If inverted match on client, then sinks are selected for
	# eg muting, thus muting the selected ps., even when not matched.
	# FIXME: This isn't good enough
	if not invert:
	    rv.extend(commands.filter_source_sink(arg, invert = invert))
	cp = commands.filter_pid(arg, invert = invert)
	cn = commands.filter_process_name(arg, invert = invert)
	ce = commands.filter_exe_name(arg, invert = invert)
		
	if pps:
	    cn = commands.filter_ptree(cn, pps)
	    logger.debug('filtered cn: %s', cn)
	    #
	    # FIXME: executable filter triggers for a inverted client match. ie handraiser 	ce = commands.filter_exe_name(arg, invert = invert)
	if pps:
	    ce = commands.filter_ptree(ce, pps)
	if invert:
	    # If any of the inverts didn't match, then none of them match.
	    if not (cp and cn and ce):
		continue
	ps = playback_streams(cp, cn, ce)
	rv.extend(ps)
    if not rv:
	print 'No targets match'
	usage()
    return set(rv)


def resolve_movable(args, pps):
    if not args:
	return sam.Client.nodes.values()
    rv = []
    for  arg in args:
 	if arg[0] == ARG_INVERT:
	    invert = True
	    arg = arg[1:]
	else:
	    invert = False
	rv.extend(commands.filter_pid(arg, invert = invert))
	cn = commands.filter_process_name(arg, invert = invert)
	if pps:
	    cn = commands.filter_ptree(cn, pps)
	rv.extend(cn)
	ce = commands.filter_exe_name(arg, invert = invert)
	if pps:
	    ce = commands.filter_ptree(ce, pps)
	rv.extend(ce)
    if not rv:
	print 'No targets match'
	usage()
    return set(rv)

def resolve_ss(arg):
    if arg[0] == ARG_INVERT:
	invert = True
	arg = arg[1:]
    else:
	invert = False
    ss = commands.filter_sources_sink(arg, invert)
    if len(ss) != 1:
	print '%d sink/source(s) match. Source can only be moved to one sink' %len(sinks)
	usage()
    return ss[0]
	
def assert_int(v):
    try:
	return int(v)
    except ValueError, e:
	usage()

def str_nodes(nodes):
    return '\n'.join([str(x) for x in nodes])
    
def main(args):
    if not args:
	usage()

    if args[0] == '-n':
	commands.	    noop = True
	args = args[1:]
    else:
	commands.noop = False
    if args[0] == '-p':
	pstree = commands.process_parents(os.getpid(), [])
	args =args[1:]
    else:
	pstree = None
    action = args[0]
    args= args[1:]
    debug= os.getenv('STFU_DEBUG')
    if debug and debug.lower() not in ('0', 'no', 'off'):
	log_level = logging.DEBUG
    else:
	log_level = logging.INFO
    logging.basicConfig(level=log_level)
	
    sam.build_sam()

    if action in ('help', 'h', '?'):
	usage()
    elif action == 'print':
	commands.print_sam()
    elif action == 'max':
	nodes = commands.blow_ears_off()
	print 'Blew ears off %s' % str_nodes(nodes)
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
	targets = resolve_targets(args[1:], pstree)
	vfn(mpy * v, targets)
	print 'Set volume for target %s' % str_nodes(targets)
    elif action == 'mute':
	targets = resolve_targets(args, pstree)
	commands.mute(True, targets)
	print 'Muted %s' % str_nodes(targets)
    elif action == 'unmute':
	targets = resolve_targets(args, pstree)
	commands.mute(False, targets)
	print 'Unmuted %s' % str_nodes(targets)
    elif  action == 'move':
	if len(args) <1:
	    usage()
	ss = resolve_ss(args[0])
	nodes = resolve_movable(args[1:], pstree)
	commands.move(nodes, ss)
	print 'Moved %s to %s' % (str_nodes(nodes), sink)
    elif action == 'default_sink':
	if len(args) != 1:
	    usage()
	sink = resolve_sink(args[0])
	if not commands.noop:
	    sink.set_default()
	print 'set default sink to: %s' % sink


    else:
	usage()
    if commands.noop:
	print 'Commands were noop'
	
    
