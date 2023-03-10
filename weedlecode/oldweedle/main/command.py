from threading import Thread
from subprocess import call
from time import sleep

class ShutdownThread(Thread):
        def __init__( self, waitFor, command ):
		super(ShutdownThread, self).__init__()
                self.waitFor = waitFor
                self.command = command

        def run( self ):
                sleep(float(self.waitFor))
                call(self.command)


class Command:
   	commandON = None
	waitFor = 0
	commandOFF = None

	def __init__(self, commandON, waitFor = None, commandOFF = None):
		self.commandON = commandON
		if ( waitFor != None and commandOFF != None ):
			self.waitFor = waitFor
 			self.commandOFF = commandOFF

	def run(self):
		call(self.commandON.split(" "))
		if ( self.commandOFF != None ):
			shutdown = ShutdownThread(self.waitFor, self.commandOFF.split(" "))
			shutdown.start()

	def __str__(self):
		if ( self.commandOFF == None ):
			return "Execute %s" % (self.commandON)
		else:
			return "Execute %s, then wait for %s seconds and execute %s" % (self.commandON, str(self.waitFor), self.commandOFF)
