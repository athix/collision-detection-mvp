from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Point3
from battleloader import BattleLoader

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable camera controls.
        self.disableMouse()

        self.battle = BattleLoader('head_on.yml', self)
        # battle.render_scene(1)
        self.derp = 1
        self.derpCounter = 0
        self.battle.render_scene(self.derp)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    # Define a procedure to mvoe the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0 ,0)
        if self.derpCounter >= 60:
            if self.derp == 0:
                self.derp = 1
            else:
                self.derp = 0
            self.battle.render_scene(self.derp)
            self.derpCounter = 0
        else:
            self.derpCounter += 1
        return Task.cont

app = MyApp()
app.run()
