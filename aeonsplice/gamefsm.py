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
            focus = 1)
    def exitMainMenu(self):
        self.battleEntry.destroy()
    def enterBattle(self, filename):
        self.statusText.setText('Battle: ' + filename)
        self.backButton = DirectButton(
            text = 'Back',
            pos = (-1, 0, -0.95),
            scale = .05,
            command = self.goBack)
        self.prevButton = DirectButton(
            text = 'Prev Turn',
            pos = (-1, 0, 0.95),
            scale = .05,
            command = self.previousTurn)
        self.nextButton = DirectButton(
            text = 'Next Turn',
            pos = (-0.70, 0, 0.95),
            scale = .05,
            command = self.nextTurn)
        self.turnText = OnscreenText(
            pos = (-0.45, 0.95),
            scale = 0.07,
            fg = (0.5, 1, 0.5, 1),
            align = TextNode.ACenter,
            mayChange = 1)
        try:
            self.battle = Battle(filename, self.app)
            self.turn = self.battle.maxTurns()
            self.battle.render_turn(self.turn)
            self.turnText.setText('Turn: ' + str(self.turn))
            if self.turn == 0:
                self.prevButton['state'] = DGG.DISABLED
                self.prevButton.hide()
            if self.turn == self.battle.maxTurns():
                self.nextButton['state'] = DGG.DISABLED
                self.nextButton.hide()
        except FileNotFoundError:
            print('Failed to load file: ', filename)
            self.forceTransition('MainMenu')
    def exitBattle(self):
        self.backButton.destroy()
        self.prevButton.destroy()
        self.nextButton.destroy()
        self.turnText.destroy()
        if hasattr(self, 'battle'):
            self.battle.reset_ships()
    def setBattle(self, textEntered):
        self.request('Battle', textEntered)
    def goBack(self):
        self.request('MainMenu')
    def previousTurn(self):
        self.turn -= 1
        self.turnText.setText('Turn: ' + str(self.turn))
        self.battle.reset_ships()
        self.battle.render_turn(self.turn)
        if self.turn == 0:
            self.prevButton['state'] = DGG.DISABLED
            self.prevButton.hide()
        if self.turn != self.battle.maxTurns():
            self.nextButton['state'] = DGG.NORMAL
            self.nextButton.show()
    def nextTurn(self):
        self.turn += 1
        self.turnText.setText('Turn: ' + str(self.turn))
        self.battle.reset_ships()
        self.battle.render_turn(self.turn)
        if self.turn != 0:
            self.prevButton['state'] = DGG.NORMAL
            self.prevButton.show()
        if self.turn == self.battle.maxTurns():
            self.nextButton['state'] = DGG.DISABLED
            self.nextButton.hide()
