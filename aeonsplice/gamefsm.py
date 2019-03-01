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
        self.app.cTraverser = CollisionTraverser()
        self.app.cHandler = CollisionHandlerQueue()
        self.app.pickerNode = CollisionNode('mouseRay')
        self.app.pickerNP = self.app.camera.attachNewNode(self.app.pickerNode)
        self.app.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.app.pickerRay = CollisionRay()
        self.app.pickerNode.addSolid(self.app.pickerRay)
        self.app.cTraverser.addCollider(self.app.pickerNP, self.app.cHandler)
        self.app.accept('mouse1', self.mouseClicky)
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
        self.deselectShip()
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
        self.deselectShip()
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
        self.deselectShip()
        self.battle.reset_ships()
        self.battle.render_turn(self.turn)
        if self.turn != 0:
            self.prevButton['state'] = DGG.NORMAL
            self.prevButton.show()
        if self.turn == self.battle.maxTurns():
            self.nextButton['state'] = DGG.DISABLED
            self.nextButton.hide()
    def mouseClicky(self):
        if hasattr(self, 'battle'):
            mpos = self.app.mouseWatcherNode.getMouse()
            self.app.pickerRay.setFromLens(self.app.camNode, mpos.getX(), mpos.getY())
            self.app.cTraverser.traverse(self.app.render)
            if self.app.cHandler.getNumEntries() > 0:
                # This is so we get the closest object.
                self.app.cHandler.sortEntries()
                pickedObj = self.app.cHandler.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag('shipID')
                if not pickedObj.isEmpty():
                    self.selectShip(pickedObj)
    def selectShip(self, obj):
        # You ever write code and immediately feel guilty for how bad it is?
        self.deselectShip()
        ship = self.battle.ships[obj.getTag('shipID')]
        player = self.battle.players[ship.player_id]
        self.shipFrame = DirectFrame(
            frameColor = (0.2, 0, 0, 1),
            frameSize = (-0.5, 0.5, -0.5, 0.5),
            pos = (0, 0, 0))
        self.closeShipButton = DirectButton(
            parent = self.shipFrame,
            text = 'Close',
            pos = (.35, 0, -.45),
            scale = .05,
            command = self.deselectShip)
        self.shipText = OnscreenText(
            parent = self.shipFrame,
            pos = (0, 0.4),
            scale = 0.07,
            fg = (0.5, 0.7, 1, 1),
            align = TextNode.ACenter,
            mayChange = 0,
            text = 'Ship: ' + ship.id)
        self.playerText = OnscreenText(
            parent = self.shipFrame,
            pos = (0, 0.3),
            scale = 0.07,
            fg = (0.5, 0.7, 1, 1),
            align = TextNode.ACenter,
            mayChange = 0,
            text = 'Player: ' + player.color)
        self.posText = OnscreenText(
            parent = self.shipFrame,
            pos = (0, 0.2),
            scale = 0.07,
            fg = (0.5, 0.7, 1, 1),
            align = TextNode.ACenter,
            mayChange = 0,
            text = 'Pos: ' + str(ship.position))
    def deselectShip(self):
        if hasattr(self, 'shipFrame'):
            self.shipFrame.destroy()
