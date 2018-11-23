import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from configurator import Ui_Configurator
from socketIO_client import SocketIO
from sprites import *
from inspect import signature
import jsonpickle
import datetime, threading, time
import random

class Configurator(Ui_Configurator):
	def __init__(self, dialog):
		self.sockets = [SocketIO('192.168.1.62', 5000), SocketIO('192.168.1.63', 5000)]
		#self.sockets = [SocketIO('127.0.0.1', 5000)]
		Ui_Configurator.__init__(self)
		self.setupUi(dialog)

		vel = Velocity(vel=(1000, 0))
		col = SpriteColorRainbow(startHue=0, transitionSpeed=0.4)
		boundDel = BoundsDelete(xLimits=(-500, 3000), yLimits=(0, 2500))
		self.sprite = SpriteModelWrapper(sockets=self.sockets,
											positionRange=[[-300, -300], [-0, 768]],
											sizeRange=[[256,256], [32,32]],
											source="img/raindrop_square.png",
											mods=[vel, col, boundDel],
											spawnIntervalRange=[80, 300])

		# Connect "add" button with a custom function (addInputTextToListbox)
		#for b in self.buttons:
			#b.clicked.connect(self.sendRequest)


	#def sendRequest(self):
		#self.socketIO.emit('add_sprites', self.buildJSON([self.sprites[0].sprite]))

class SpriteModelWrapper(object):
	#sockets: an array of SocketIO clients to emit through
	#sprite: the SpriteJSONModel to send
	#spawnIntervalRange: a two element array containing the lower and upper bound of time in milliseconds between spawns
	def __init__(self, sockets, positionRange, sizeRange, source, mods, spawnIntervalRange):
		self.sockets = sockets
		self.positionRange = positionRange
		self.sizeRange = sizeRange
		self.source = source
		self.mods = mods
		self.spawnIntervalRange = spawnIntervalRange
		self.targetTime = time.time()
		self.spawnPeriodically()

	def spawnPeriodically(self):
		xPos = random.randint(self.positionRange[0][0], self.positionRange[0][1])
		yPos = random.randint(self.positionRange[1][0], self.positionRange[1][1])
		xSize = random.randint(self.sizeRange[0][0], self.sizeRange[0][1])
		ySize = random.randint(self.sizeRange[1][0], self.sizeRange[1][1])
		sprite = SpriteJSONModel(pos=(xPos, yPos), size=(xSize, ySize), source=self.source, mods=self.mods)
		for socket in self.sockets:
			socket.emit('add_sprites', jsonpickle.encode([sprite], unpicklable=False))
		self.targetTime = self.targetTime + random.randint(self.spawnIntervalRange[0], self.spawnIntervalRange[1])/1000
		threading.Timer(self.targetTime - time.time(), self.spawnPeriodically).start()


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QMainWindow()

	prog = Configurator(dialog)

	dialog.show()
	sys.exit(app.exec_())
