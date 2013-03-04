# Exec commands on sam
# TODO:
# Review use of gens + iters. Maybe iterate the list once and pass a list of filter fns.
# Add negate arg to re filters. Inverts sense of match, parse !foo from command line.

import sys, os, re, logging

import sam

logger = logging.getLogger('__main__')

def filter_all():
    for node in sam.Sink.nodes.values() + sam.PlaybackStream.nodes.values():
	yield node

def filter_clients():
    for node in sam.Client.nodes.values():
	yield node
	
def filter_pid(pid, nodes = None):
    if not nodes:
	nodes = filter_clients()
    for node in nodes:
	logger.debug('pid cmp %r %r', node.a_pid, pid)
	if node.a_pid == pid:
	    yield node

def filter_re(res, attr, nodes = None):
    if not nodes:
	nodes = filter_clients()
    cre = re.compile(res, re.I)
    for node in nodes:
	match = cre.search(getattr(node,attr))
	if match:
	    yield node

def 	 filter_process_name(name, nodes = None):
    for x in filter_re(name, 'a_name', nodes):
	yield x
	
def 	 filter_exe_name(name, nodes = None):
    for x in filter_re(name, 'a_exe', nodes):
	yield x


def filter_sink(name):
    rv = []
    cre = re.compile(name, re.I)
    for sink in sam.Sink.nodes.values():
	match = cre.search(sink.name)
	if match:
	    rv.append(sink)
    return rv   
    
def blow_ears_off(nodes = None):
    if not nodes:
	nodes = filter_all()
    for node in nodes:
	logger.debug('beo: %s', node)
	node.mute = False
	node.volume = 2**16

def set_volume(v, nodes = None):
    if not nodes:
	nodes = filter_all()
    for node in nodes:
	logger.debug('Set volume %s to %d', node, v)
	node.mute = False
	node.volume = v

def incr_volume(i, nodes = None):
    if not nodes:
	nodes = filter_all()
    for node in nodes:
	node.volume += i
	logger.debug('Incr Volume: %d for %s', node.volume, node)


def mute(v, nodes):
    if not nodes:
	nodes = filter_all()
    for node in nodes:
	logger.debug('nuting %s %s', v, ps)
	node.mute = v


def move(clients, sink):
    for client in clients:
	for ps in client.playback_links:
	    ps.move(sink)
	    

def print_sam():
    for k, v in sam.Sink.nodes.items():
	print v
    for k, v  in sam.Client.nodes.items():
	print v.a_pid, '\t', v.a_name, '\t', v.a_exe, '\t',
	for ps in v.playback_links:
	    print '\t', ps.sink_link.name,
	print

		


if __name__ == '__main__':
    if os.getenv('STFU_DEBUG'):
	logging.basicConfig(level=logging.DEBUG)
    sam.build_sam()
    print_sam()
    print '*' * 80
    clients = filter_process_name(sys.argv[1])
    #print 'clients:', '\n'.join([str(x) for x in clients])
    sink = filter_sink(sys.argv[2])
    print sink
    move(clients, sink)
    
#    for x in filter_process_name(sys.argv[1]):
#	print x
#	#    print sam.Sink.nodes.keys()
#    spkr = sam.Sink.nodes['/org/pulseaudio/core1/sink%s' % sys.argv[2]]
#    move(filter_process_name(sys.argv[1]), spkr)

