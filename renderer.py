from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle
import random
from functools import partial
from kivy.clock import Clock
from kivy.core.image import Image
from flask import Flask, jsonify, request
import json
import threading
from multiprocessing import Process
import os
from sprites import *
from concurrent.futures import ThreadPoolExecutor
from flask_socketio import SocketIO
from inspect import signature
import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 5000        # Port to listen on (non-privileged ports are > 1023)

class Renderer(App):
    def __init__(self, wid, *args, **kwargs):
        super(Renderer, self).__init__(*args, **kwargs)
        self.wid = wid

    def addMovingRaindrop(self, *largs):
        rect = Sprite(pos=(-512, random.randint(0, 1440)), size=(256, 32), source='img/raindrop_square.png')
        mod = Velocity(vel=(random.randint(1200, 2000),0))
        col = SpriteColorRainbow(startingColor=Color(random.uniform(0, 1), 1, 1, mode='hsv'), transitionSpeed=0.3)
        bound = BoundsDelete(xLimits=[-1000, 3000], yLimits=[0, 1440])
        animSize = AnimatedSize(speed=-0.8)
        rect.addModifiers([mod, col, bound, animSize])
        self.wid.add(rect)


    def build(self):
        #wid = SpriteManager()

        root = BoxLayout(orientation='vertical')
        root.add_widget(self.wid)

        #Clock.schedule_interval(partial(self.add_rects, 1), 1)
        #self.add_rects(1)
        self.addMovingRaindrop() #seems like a needed initialization step for future sprites to be added
        #Clock.schedule_interval(partial(self.addMovingRaindrop), 1.0/0.1)
        Clock.schedule_interval(partial(self.wid.update), 1.0/60.0)

        return root

def parseAddSpriteJSON(jsonArr):
    sprites = []
    for s in jsonArr:
        modParms = s["mods"]
        del s["mods"]
        sprite = Sprite(**s)
        mods = parseModJSON(modParms)
        sprite.addModifiers(mods)
        sprites.append(sprite)

    return sprites

def parseModJSON(jsonArr):
    mods = []
    for m in jsonArr:
        for mod in SpriteModifier.__subclasses__():
            parms = list(signature(mod.__init__).parameters)
            parms.remove("self")
            parms.remove("kwargs")
            if arrayContentsEqual(parms, list(m.keys())):
                mods.append(mod(**m))

    return mods

#makes it so the arrays don't need matching orders
def arrayContentsEqual(arr1, arr2):
    if len(arr1) != len(arr2):
        return False

    for a in arr1:
        if a not in arr2:
            return False

    return True


kivyApp = Renderer(SpriteManager())

def start_websocket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                jsonString = data.decode()
                sprites = parseAddSpriteJSON(json.loads(jsonString))
                for s in sprites:
                    kivyApp.wid.add(s)

                #conn.sendall(data)


if __name__ == '__main__':
    t = threading.Thread(target=start_websocket)
    t.setDaemon(True)
    t.start()
    kivyApp.run()
