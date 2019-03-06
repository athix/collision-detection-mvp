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

        # TODO: Support manual camera control (WASD&CTRL/SPACE + Mouse)

        self.gameFSM = GameFSM(self)
        self.gameFSM.request('MainMenu')

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0 ,0)
        return Task.cont

app = MyApp()
app.run()
