import sys, os, re, logging, operator
import psutil
import sam

logger = logging.getLogger('__main__')
noop = False

def process_parents(pid, result):
    p = psutil.Process(pid)
    for c in p.get_children():
	result.append(c)
    if p.ppid != 1:
	result = process_parents(p.ppid, result)
    return result

def filter_ptree(clients, processes):
    rv = []
    pid_list = [x.pid for x in processes]
    logger.debug('parent pid  list: %s', pid_list)
    for  client in clients:
	logger.debug('xxxxx %s', client.a_name)
	if client.a_pid in pid_list:
	    logger.debug('adding %s', client)
	    rv.append(client)
    return rv

def filter_controllable():
    return sam.Sink.nodes.values() + sam.PlaybackStream.nodes.values() + sam.Source.nodes.values() 

def filter_clients():
    return sam.Client.nodes.values()
	
def filter_pid(pid, clients = None, invert = False):
    if not clients:
	clients = filter_clients()
    op = operator.ne if invert else operator.eq
    return [x for x in clients if op(x.a_pid, pid)]

def filter_re(res, attr, clients = None, invert = False):
    if not clients:
	clients = filter_clients()
    cre = re.compile(res, re.I)
    # invert means == None
    op = operator.eq if invert else operator.ne
    rv = []
    for client in clients:
	n = getattr(client, attr)
	logger.debug('re cmp %s/%s/%s/%s|', op, attr, n, client)
	if n and  op(cre.search(n), None):
	    logger.debug('re cmp matched %r', cre.search(n))
	    rv.append(client)
    return rv

def 	 filter_process_name(name, clients = None, invert = False):
    return filter_re(name, 'a_name', clients, invert)
	
def 	 filter_exe_name(name, clients = None, invert = False):
    return filter_re(name, 'a_exe', clients, invert)


def _filter_klass(klass, name, invert = False):
    cre = re.compile(name, re.I)
    # invert means == None
    op = operator.eq if invert else operator.ne
    return [x for x in klass.nodes.values() if op(cre.search(x.name), None)]


def filter_sink(name, invert = False):
    return _filter_klass(sam.Sink, name, invert)

def filter_source(name, invert = False):
    return _filter_klass(sam.Source, name, invert)

def filter_source_sink(name, invert = False):
    # FIXME: Think about what invert means in this case
    return filter_source(name, invert) + filter_sink(name, invert)
    
def blow_ears_off(nodes = None):
    if not nodes:
	nodes = filter_controllable()
    for node in nodes:
	logger.debug('beo: %s', node)
	if not noop:
	    node.mute = False
	    node.volume = 2**16
    return nodes
    

def set_volume(v, nodes = None):
    if not nodes:
	nodes = filter_controllable()
    for node in nodes:
	logger.debug('Set volume %s to %d', node, v)
	if not noop:
	    node.mute = False
	    node.volume = v
    return nodes
    

def incr_volume(i, nodes = None):
    if not nodes:
	nodes = filter_controllable()
    for node in nodes:
	if not noop:
	    node.volume += i
	logger.debug('Incr Volume: %d for %s', node.volume, node)
    return nodes


def mute(v, nodes):
    if not nodes:
	nodes = filter_contrallable()
    for node in nodes:
	logger.debug('nuting %s %s', v, node)
	if not noop:
	    node.mute = v
    return nodes

def move(clients, sink):
    for client in clients:
	for ps in client.playback_links:
	    if not noop:
		ps.move(sink)
	    

def print_sam():
    print 'SINKS', sam.Sink.get_default()
    for k, v in sam.Sink.nodes.items():
	print v
    print 'Sources:'
    for k, v in sam.Source.nodes.items():
	print v
    print 'CLIENTS'
    for k, v  in sam.Client.nodes.items():
	print v.a_pid, '\t', v.a_name, '\t', 
	for ps in v.playback_links:
	    print '\t', ps.sink_link.name,
	for rs in v.record_links:
	    print '\t', rs.source_link.name,
	print

		

