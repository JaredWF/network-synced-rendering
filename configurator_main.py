import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from configurator import Ui_Configurator
from socketIO_client import SocketIO
from sprites import *
from inspect import signature
import jsonpickle

class Configurator(Ui_Configurator):
	def __init__(self, dialog):
		self.socketIO = SocketIO('127.0.0.1', 5000)
		Ui_Configurator.__init__(self)
		self.setupUi(dialog)

		# Connect "add" button with a custom function (addInputTextToListbox)
		for b in self.buttons:
			b.clicked.connect(self.sendRequest)


	def buildDummyJSON(self):
		vel = Velocity(vel=(3000, 0))
		col = SpriteColor(r=0, g=1, b=1, a=1)
		boundDel = BoundsDelete(xLimits=(-500, 3000), yLimits=(0, 2500))
		sprite = SpriteModel(pos=(-300, 800), size=(256, 32), source="img/raindrop_square.png", mods=[vel, col, boundDel])
		return jsonpickle.encode([sprite], unpicklable=False)


	def sendRequest(self):
		self.socketIO.emit('add_sprites', self.buildDummyJSON())


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QMainWindow()

	prog = Configurator(dialog)

	dialog.show()
	sys.exit(app.exec_())
