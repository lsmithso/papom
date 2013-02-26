# Exec commands on sam

import sys, os, re, logging

import sam

logger = logging.getLogger(__name__)

def blow_ears_off():
    for node in sam.Sink.nodes.values() + sam.PlaybackStream.nodes.values():
	node.nute = False
	node.volume = 2**16
	logger.debug('Nax Unmuted %s', node)

	
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sam.build_sam()
    blow_ears_off()
	
