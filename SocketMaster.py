from socketIO_client import SocketIO, LoggingNamespace

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_aaa_response(*args):
    print('on_aaa_response', args)

socketIO = SocketIO('127.0.0.1', 5000)
print(socketIO)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)
socketIO.emit('add_sprites', '[ 	{ 		"pos": [-300, 800], 		"size": [256, 32], 		"source": "img/raindrop_square.png", 		"mods": [ 			{ 				"name":"velocity", 				"vel":[3000, 0] 			}, 			{ 				"name":"color", 				"r": 0, 				"g": 1, 				"b": 1, 				"a": 1 			}, 			{ 				"name":"bounds", 				"xLimits":[-500, 3000], 				"yLimits":[0, 2500] 			} 			] 	}, 	{ 		"pos": [-300, 600], 		"size": [256, 32], 		"source": "img/raindrop_square.png", 		"mods": [ 			{ 				"name":"velocity", 				"vel":[2000, 0] 			}, 			{ 				"name":"color", 				"r": 0, 				"g": 1, 				"b": 1, 				"a": 1 			}, 			{ 				"name":"bounds", 				"xLimits":[-500, 3000], 				"yLimits":[0, 2500] 			} 			] 	}, 	{ 		"pos": [-300, 400], 		"size": [256, 32], 		"source": "img/raindrop_square.png", 		"mods": [ 			{ 				"name":"velocity", 				"vel":[1000, 0] 			}, 			{ 				"name":"color", 				"r": 0, 				"g": 1, 				"b": 1, 				"a": 1 			}, 			{ 				"name":"bounds", 				"xLimits":[-500, 3000], 				"yLimits":[0, 2500] 			} 			] 	} ]')
