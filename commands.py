# Exec commands on sam

import sys, os, re, logging

import sam

logger = logging.getLogger('x')

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
	logger.debug('Volume: %d for %s', node.volume, node)


def mute(v, nodes):
    if not nodes:
	nodes = filter_all()
    for node in nodes:
	print 'xxxxxx', node, node.playback_links
	for ps in node.playback_links:
	    print 'xxxxx', ps
	    logger.debug('nuting %s %s', v, ps)
	    ps.mute = v


def print_sam():
    for k, v  in sam.Client.nodes.items():
	print v.a_pid, '\t', v.a_name, '\t', v.a_exe, '\t',
	for ps in v.playback_links:
	    print '\t', ps.sink_link.name,
	print

		


if __name__ == '__main__':
    #    logging.basicConfig(level=logging.DEBUG)
    sam.build_sam()
    print_sam()
    ai = int(sys.argv[1])
    #    blow_ears_off()
    #    set_volume_all(intai)
    #    incr_volume_all(ai)
    print [str(x) for x in filter_pid(ai)]
    v = True if sys.argv[2] == '1' else False
    mute(v, filter_pid(ai))
    
    
