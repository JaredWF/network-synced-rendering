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


class Renderer(App):
    def __init__(self, wid, *args, **kwargs):
        super(Renderer, self).__init__(*args, **kwargs)
        self.wid = wid


    def add_rects(self, count, *largs):
        for x in range(count):
            scale = random.uniform(0.3, 1)
            rect = MovingSprite(canvas=self.wid.canvas, color=Color(random.uniform(0, 1), 1, 1, mode='hsv'),
                                                   vel=(30, 0),
                                                   xLimits=[-1000, 2000],
                                                   yLimits=[-500, 1500],
                                                   pos=(-512, random.randint(0, 1080)),
                                                   size=(256*scale, 32*scale),
                                                   source='img/raindrop_square.png')
            self.wid.add(rect)

    def addMovingRaindrop(self, *largs):
        rect = Sprite(pos=(-512, random.randint(0, 1440)), size=(256, 32), source='img/raindrop_square.png')
        mod = Velocity(vel=(1500,0))
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
        self.addMovingRaindrop()
        #Clock.schedule_interval(partial(self.addMovingRaindrop), 1.0/5.0)
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
        name = m["name"]
        del m["name"]
        if name == "velocity":
            mods.append(Velocity(**m))
        elif name == "color":
            mods.append(SpriteColor(**m))
        elif name == "bounds":
            mods.append(BoundsDelete(**m))

    return mods


kivyApp = Renderer(SpriteManager())
app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/create_sprite', methods=['POST'])
def create_sprite():
    content = request.json
    #kivyApp.addMovingRaindrop()
    sprites = parseAddSpriteJSON(content)
    for s in sprites:
        kivyApp.wid.add(s)

    return "success"

@socketio.on('add_sprites')
def test_message(message):
    sprites = parseAddSpriteJSON(json.loads(message))
    for s in sprites:
        kivyApp.wid.add(s)

def start_app():
    print("Starting Flask app...")
    socketio.run(app, port=5000, host='0.0.0.0')
    #socketio.run(app, port=5000, host='127.0.0.1')
    #app.run(port=5000, debug=False, host='0.0.0.0')     #specify separate port to run Flask app


if __name__ == '__main__':
    t = threading.Thread(target=start_app)
    t.setDaemon(True)
    t.start()
    kivyApp.run()
