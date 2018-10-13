from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle
import random
from functools import partial
from kivy.clock import Clock
from kivy.vector import Vector
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.core.image import Image
from flask import Flask, jsonify, request
import threading
from multiprocessing import Process
import os


class MovingSprite(Rectangle):
    def __init__(self, canvas, color, vel, xLimits, yLimits, **kwargs):
        super(MovingSprite, self).__init__(**kwargs)
        self.canvas = canvas
        self.color = color
        self.vel = vel
        self.canvas.add(self)
        self.xLimits = xLimits
        self.yLimits = yLimits

    def update(self):
        self.move()

    def move(self):
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])

    def readyToDestroy(self):
        if self.pos[0] < self.xLimits[0]:
            return True
        elif self.pos[0] > self.xLimits[1]:
            return True
        elif self.pos[1] < self.yLimits[0]:
            return True
        elif self.pos[1] > self.yLimits[1]:
            return True

        return False


class Sprite(Rectangle):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)

    def setManager(self, manager):
        self.manager = manager

    def addModifiers(self, modifiers):
        self.modifiers = modifiers
        for m in self.modifiers:
            m.setSprite(self)

    def addToCanvas(self):
        for m in self.modifiers:
            if m.getCanvasComponent():
                self.manager.canvas.add(m.getCanvasComponent())
        self.manager.canvas.add(self)

    def removeFromCanvas(self):
        self.manager.canvas.remove(self) #maybe do this twice?
        for m in self.modifiers:
            if m.getCanvasComponent():
                self.manager.canvas.remove(m.getCanvasComponent())


    def update(self, dt):
        for m in self.modifiers:
            m.update(dt)


class SpriteModifier: #make factory method so you don't have to pass in sprite
    def __init__(self):
        pass

    def setSprite(self, sprite):
        self.sprite = sprite

    def update(self, dt):
        pass

    def getCanvasComponent(self):
        pass

class Velocity(SpriteModifier):
    def __init__(self, vel, **kwargs):
        super(Velocity, self).__init__(**kwargs)
        self.vel = vel
        #self.vel = ReferenceListProperty(NumericProperty(vel[0]), NumericProperty(vel[1]))

    def update(self, dt):
        self.sprite.pos = (self.sprite.pos[0] + dt*self.vel[0], self.sprite.pos[1] + dt*self.vel[1])

    def getCanvasComponent(self):
        return None

class SpriteColor(SpriteModifier):
    def __init__(self, r, g, b, a, **kwargs):
        super(SpriteColor, self).__init__(**kwargs)
        self.color = Color(r, g, b, a)

    def getCanvasComponent(self):
        return self.color

class SpriteColorRainbow(SpriteModifier):
    def __init__(self, startingColor, transitionSpeed, **kwargs):
        super(SpriteColorRainbow, self).__init__(**kwargs)
        self.color = startingColor
        self.transitionSpeed = transitionSpeed

    def getCanvasComponent(self):
        return self.color

    def update(self, dt):
        temp = self.color.h - dt * self.transitionSpeed
        if temp <= 0.001:
            temp = 0.998
        elif temp >= 0.999:
            temp = 0.002
        self.color.h = temp

class AnimatedSize(SpriteModifier):
    def __init__(self, speed, **kwargs):
        super(AnimatedSize, self).__init__(**kwargs)
        self.speed = speed

    def getCanvasComponent(self):
        return None

    def update(self, dt):
        self.sprite.size = (self.sprite.size[0] + self.sprite.size[0] * dt * self.speed, self.sprite.size[1] + self.sprite.size[1] * dt * self.speed)

class BoundsDelete(SpriteModifier):
    def __init__(self, xLimits, yLimits, **kwargs):
        super(BoundsDelete, self).__init__(**kwargs)
        self.xLimits = xLimits
        self.yLimits = yLimits

    def getCanvasComponent(self):
        return None

    def update(self, dt):
        posX = self.sprite.pos[0]
        posY = self.sprite.pos[1]
        if posX < self.xLimits[0] or posX > self.xLimits[1]:
            self.sprite.manager.removeSprite(self.sprite)
        elif posY < self.xLimits[0] or posY > self.yLimits[1]:
            self.sprite.manager.removeSprite(self.sprite)



class SpriteManager(Widget):
    def __init__(self, **kwargs):
        super(SpriteManager, self).__init__(**kwargs)
        self.sprites = []

    def update(self, dt):
        for s in self.sprites:
            s.update(dt)
            #if s.readyToDestroy():
                #self.canvas.remove(s.color)
                #self.canvas.remove(s)
                #self.canvas.remove(s)
                #self.sprites.remove(s)

    def removeSprite(self, sprite):
        self.sprites.remove(sprite)
        sprite.removeFromCanvas()

    def add(self, sprite):
        sprite.setManager(self)
        sprite.addToCanvas()
        self.sprites.append(sprite)
