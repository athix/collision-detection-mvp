from direct.fsm.FSM import FSM
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from battle import Battle

class GameFSM(FSM):
    def __init__(self, app):
        FSM.__init__(self, 'GameFSM')
        self.app = app
        self.statusText = OnscreenText(
            pos = (0.95, -0.95),
            scale = 0.07,
            fg = (1, 0.5, 0.5, 1),
            align = TextNode.ACenter,
            mayChange = 1)
        self.defaultTransitions = {
            'MainMenu': ['Battle'],
            'Battle': ['MainMenu']}
    def enterMainMenu(self):
        self.statusText.setText('Main Menu')
        self.battleEntry = DirectEntry(
            text = '',
            scale = .05,
            command = self.setBattle,
            numLines = 1,
            focus = 0)
    def exitMainMenu(self):
        self.battleEntry.destroy()
    def enterBattle(self, filename):
        self.statusText.setText('Battle: ' + filename)
        self.backButton = DirectButton(
            text = 'Back',
            pos = (-0.95, 0, -0.95),
            scale = .05,
            command = self.goBack)
        try:
            self.battle = Battle(filename, self.app)
            self.battle.render_turn(0)
        except:
            print('Failed to load file: ', filename)
            self.forceTransition('MainMenu')
    def exitBattle(self):
        self.backButton.destroy()
        if hasattr(self, 'battle'):
            self.battle.reset_ships()
    def setBattle(self, textEntered):
        self.request('Battle', textEntered)
    def goBack(self):
        self.request('MainMenu')
