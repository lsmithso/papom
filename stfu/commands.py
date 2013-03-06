# Exec commands on sam
# TODO:
# Review use of gens + iters. Maybe iterate the list once and pass a list of filter fns.
# Add negate arg to re filters. Inverts sense of match, parse !foo from command line.

import sys, os, re, logging

import stfu
import sam

logger = logging.getLogger('__main__')

def filter_controllable():
    return sam.Sink.nodes.values() + sam.PlaybackStream.nodes.values()

def filter_clients():
    return sam.Client.nodes.values()
	
def filter_pid(pid, clients = None):
    if not clients:
	clients = filter_clients()
    return [x for x in clients if x.a_pid == pid]

def filter_re(res, attr, clients = None):
    if not clients:
	clients = filter_clients()
    cre = re.compile(res, re.I)
    rv = []
    for client in clients:
	n = getattr(client, attr)
	if n and  cre.search(n):
	    rv.append(client)
    return rv

def 	 filter_process_name(name, clients = None):
    return filter_re(name, 'a_name', clients)
	
def 	 filter_exe_name(name, clients = None):
    return filter_re(name, 'a_exe', clients)

def filter_sink(name):
    cre = re.compile(name, re.I)
    return [x for x in sam.Sink.nodes.values() if cre.search(x.name)]
    
def blow_ears_off(nodes = None):
    if not nodes:
	nodes = filter_controllable()
    for node in nodes:
	logger.debug('beo: %s', node)
	node.mute = False
	node.volume = 2**16
    return nodes
    

def set_volume(v, nodes = None):
    if not nodes:
	nodes = filter_controllable()
    for node in nodes:
	logger.debug('Set volume %s to %d', node, v)
	node.mute = False
	node.volume = v
    return nodes
    

def incr_volume(i, nodes = None):
    if not nodes:
	nodes = filter_controllable()
    for node in nodes:
	node.volume += i
	logger.debug('Incr Volume: %d for %s', node.volume, node)
    return nodes


def mute(v, nodes):
    if not nodes:
	nodes = filter_contrallable()
    for node in nodes:
	logger.debug('nuting %s %s', v, node)
	node.mute = v
    return nodes

def move(clients, sink):
    for client in clients:
	for ps in client.playback_links:
	    ps.move(sink)
	    

def print_sam():
    print 'SINKS'
    for k, v in sam.Sink.nodes.items():
	print v
    print 'CLIENTS'
    for k, v  in sam.Client.nodes.items():
	print v.a_pid, '\t', v.a_name, '\t', v.a_exe, '\t',
	for ps in v.playback_links:
	    print '\t', ps.sink_link.name,
	print

		

