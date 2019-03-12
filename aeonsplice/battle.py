import yaml

class Battle:
    def __init__(self, filename, app):
        # Open and parse YAML file with battle data
        with open(filename, 'r') as stream:
            try:
                self.data = yaml.safe_load(stream)
            except yaml.YAMLError as error:
                print(error)

        # Initialize instance variables
        self.app = app
        self.players = {}
        self.output_filename = filename
        self.current_turn = None

        # Load players from file data
        for player in self.data['players']:
            temp = Player(player)
            self.players[temp.id] = temp

    def render_turn(self, turn):
        turn_data = self.data['turns'][turn]
        if turn != turn_data['time']:
            raise Exception('Invalid battle data, turn does not match time!')
        # (re)set self.ships
        self.reset_ships()
        # Load and render ships
        for ship in turn_data['ships']:
            temp = Ship(ship)
            temp.render(self.app)
            self.ships[temp.id] = temp
        # Save current turn for reference in other functions
        self.current_turn = turn

    def reset_ships(self):
        if hasattr(self, 'ships'):
            for key, ship in self.ships.items():
                ship.remove()
        self.ships = {}

    def maxTurns(self):
        return (len(self.data['turns']) - 1)

    def saveToFile(self):
        with open(self.output_filename, 'w') as stream:
            yaml.dump(self.data, stream, default_flow_style=False)

class Player:
    def __init__(self, player_data):
        self.id = player_data['id']
        self.color = player_data['color']

class Ship:
    def __init__(self, ship_data):
        self.id = ship_data['id']
        self.player_id = ship_data['player_id']
        self.position = ship_data['position']
        if 'move' in ship_data:
            self.move = ship_data['move']
        else:
            self.move = None
        self.model_filename = self.getModelFilename(self.id)
        self.x = self.position['x']
        self.y = self.position['y']
        self.z = self.position['z']
        if self.move is not None:
            self.dx = self.move['x']
            self.dy = self.move['y']
            self.dz = self.move['z']
        else:
            self.dx = 0
            self.dy = 0
            self.dz = 0

    def getModelFilename(self, ship_id):
        models = {
            'cube': 'models/frowney',
            'sphere': 'models/smiley'
        }
        return models.get(ship_id, 'models/panda')

    def render(self, app):
        self.model = app.loader.loadModel(self.model_filename)
        self.model.reparentTo(app.render)
        self.model.setScale(0.25, 0.25, 0.25)
        self.model.setPos(self.x, self.y, self.z)
        self.model.setTag('shipID', self.id)

    def saveMove(self, battle):
        ships = battle.data['turns'][battle.current_turn]['ships']
        for ship in ships:
            if ship['id'] == self.id:
                ship_index = ships.index(ship)
        battle.data['turns'][battle.current_turn]['ships'][ship_index]['move'] = {
            'x':self.dx,
            'y':self.dy,
            'z':self.dz}
    def remove(self):
        self.model.removeNode()
