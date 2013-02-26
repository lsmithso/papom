# Exec commands on sam

import sys, os, re, logging

import sam

logger = logging.getLogger(__name__)

def blow_ears_off():
    for node in sam.Sink.nodes.values() + sam.PlaybackStream.nodes.values():
	logger.debug('Nax Unmuted %s', node)
		
	node.nute = False
	node.volume = 50000

	
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sam.build_sam()
    blow_ears_off()
	
