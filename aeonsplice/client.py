from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from battleloader import BattleLoader

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable camera controls.
        self.disableMouse()

        self.textObject = OnscreenText(
            pos = (0.95, -0.95),
            scale = 0.07,
            fg = (1, 0.5, 0.5, 1),
            align = TextNode.ACenter,
            mayChange = 1)

        self.entry = DirectEntry(
            text = "",
            scale = .05,
            command = self.setText,
            numLines = 1,
            focus = 0)

        # self.battle = BattleLoader('head_on.yml', self)
        # battle.render_scene(1)
        # self.derp = 1
        # self.derpCounter = 0
        # self.battle.render_scene(self.derp)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def setText(self, textEntered):
        self.textObject.setText(textEntered)
        if hasattr(self, 'battle'):
            self.battle.clear_scene()
        self.battle = BattleLoader(textEntered, self)
        self.battle.render_scene(0)

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
