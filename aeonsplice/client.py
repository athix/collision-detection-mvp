from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
# from battleloader import BattleLoader
from battle import Battle
from gamefsm import GameFSM

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable camera controls.
        self.disableMouse()

        self.gameFSM = GameFSM(self)
        self.gameFSM.request('MainMenu')

        # self.battle = BattleLoader('head_on.yml', self)
        # battle.render_scene(1)
        # self.derp = 1
        # self.derpCounter = 0
        # self.battle.render_scene(self.derp)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # def setText(self, textEntered):
    #     self.textObject.setText(textEntered)
    #     if hasattr(self, 'battle'):
    #         self.battle.reset_ships()
    #     try:
    #         self.battle = Battle(textEntered, self)
    #         self.battle.render_turn(0)
    #     except FileNotFoundError:
    #         print('Failed to load file: ', textEntered)

    # Define a procedure to mvoe the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0 ,0)
        # if self.derpCounter >= 60:
        #     if self.derp == 0:
        #         self.derp = 1
        #     else:
        #         self.derp = 0
        #     self.battle.render_scene(self.derp)
        #     self.derpCounter = 0
        # else:
        #     self.derpCounter += 1
        return Task.cont

app = MyApp()
app.run()
