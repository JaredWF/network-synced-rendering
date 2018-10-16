import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from configurator import Ui_Configurator
from socketIO_client import SocketIO
from sprites import *
from inspect import signature

class Configurator(Ui_Configurator):
	def __init__(self, dialog):
		self.socketIO = SocketIO('127.0.0.1', 5000)
		Ui_Configurator.__init__(self)
		self.setupUi(dialog)

		# Connect "add" button with a custom function (addInputTextToListbox)
		for b in self.buttons:
			b.clicked.connect(self.sendRequest)


	def sendRequest(self):
		self.socketIO.emit('add_sprites', """[
	{
		"pos": [-300, 800],
		"size": [256, 32],
		"source": "img/raindrop_square.png",
		"mods": [
			{
				"vel":[3000, 0]
			},
			{
				"r": 0,
				"g": 1,
				"b": 1,
				"a": 1
			},
			{
				"xLimits":[-500, 3000],
				"yLimits":[0, 2500]
			}
			]
	},
	{
		"pos": [-300, 600],
		"size": [256, 32],
		"source": "img/raindrop_square.png",
		"mods": [
			{
				"vel":[2000, 0]
			},
			{
				"r": 0,
				"g": 1,
				"b": 1,
				"a": 1
			},
			{
				"xLimits":[-500, 3000],
				"yLimits":[0, 2500]
			}
			]
	},
	{
		"pos": [-300, 400],
		"size": [256, 32],
		"source": "img/raindrop_square.png",
		"mods": [
			{
				"vel":[1000, 0]
			},
			{
				"g": 1,
				"r": 0,
				"b": 1,
				"a": 1
			},
			{
				"xLimits":[-500, 3000],
				"yLimits":[0, 2500]
			}
			]
	}
]""")


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QMainWindow()

	prog = Configurator(dialog)

	dialog.show()
	sys.exit(app.exec_())



#[('__class__', <class 'type'>), ('__dict__', mappingproxy({'__module__': 'sprites', '__init__': <function Velocity.__init__ at 0x04898B70>, 'update': <function Velocity.update at 0x04898BB8>, 'getCanvasComponent': <function Velocity.getCanvasComponent at 0x04898C00>, '__doc__': None})), ('__doc__', None), ('__module__', 'sprites'), ('__weakref__', <attribute '__weakref__' of 'SpriteModifier' objects>)]
