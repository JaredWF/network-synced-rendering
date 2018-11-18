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
		#self.sockets = [SocketIO('192.168.1.62', 5000), SocketIO('192.168.1.63', 5000)]
		self.sockets = [SocketIO('127.0.0.1', 5000)]
		Ui_Configurator.__init__(self)
		self.setupUi(dialog)
		tempSprites = self.buildTestSprites()
		self.sprites = []
		self.sprites.append(SpriteModelWrapper(self.sockets, tempSprites[0], [500, 2000]))
		self.sprites.append(SpriteModelWrapper(self.sockets, tempSprites[1], [500, 2000]))
		self.sprites.append(SpriteModelWrapper(self.sockets, tempSprites[2], [500, 2000]))

		# Connect "add" button with a custom function (addInputTextToListbox)
		#for b in self.buttons:
			#b.clicked.connect(self.sendRequest)

	def buildTestSprites(self):
		vel = Velocity(vel=(1000, 0))
		col = SpriteColorRainbow(transitionSpeed=0.3)
		red = SpriteColor(r=1, g=0, b=0, a=1)
		boundDel = BoundsDelete(xLimits=(-500, 2300), yLimits=(0, 2500))
		redSprite = SpriteJSONModel(pos=(-300, 100), size=(256, 32), source="img/raindrop_square.png", mods=[vel, col, boundDel])
		greenSprite = SpriteJSONModel(pos=(-300, 400), size=(256, 32), source="img/raindrop_square.png", mods=[vel, col, boundDel])
		blueSprite = SpriteJSONModel(pos=(-300, 700), size=(256, 32), source="img/raindrop_square.png", mods=[vel, col, boundDel])
		return [redSprite, greenSprite, blueSprite]

	def buildJSON(self, sprites):
		return jsonpickle.encode(sprites, unpicklable=False)


	#def sendRequest(self):
		#self.socketIO.emit('add_sprites', self.buildJSON([self.sprites[0].sprite]))

class SpriteModelWrapper(object):
	#sockets: an array of SocketIO clients to emit through
	#sprite: the SpriteJSONModel to send
	#spawnIntervalRange: a two element array containing the lower and upper bound of time in milliseconds between spawns
	def __init__(self, sockets, sprite, spawnIntervalRange):
		self.sockets = sockets
		self.sprite = sprite
		self.spawnIntervalRange = spawnIntervalRange
		self.targetTime = time.time()
		self.spawnPeriodically()

	def spawnPeriodically(self):
		for socket in self.sockets:
			socket.emit('add_sprites', jsonpickle.encode([self.sprite], unpicklable=False))
		self.targetTime = self.targetTime + random.randint(self.spawnIntervalRange[0], self.spawnIntervalRange[1])/1000
		threading.Timer(self.targetTime - time.time(), self.spawnPeriodically).start()


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QMainWindow()

	prog = Configurator(dialog)

	dialog.show()
	sys.exit(app.exec_())
