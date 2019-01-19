import yaml

class Ship:
    def __init__(self, options):
        self.id = options['id']
        self.model_file = self.getModelFile(options['model'])

    def getModelFile(self, model):
        known_models = {
            'cube': "models/frowney",
            'sphere': "models/smiley"
        }
        return known_models.get(model, "models/panda")

    def attach(self, app):
        self.model = app.loader.loadModel(self.model_file)
        self.model.reparentTo(app.render)
        self.model.setScale(0.25, 0.25, 0.25)

    def detach(self):
        self.model.removeNode()

    def setPosition(self, position):
        x = position['x']
        y = position['y']
        z = position['z']
        self.model.setPos(x, y, z)

class BattleLoader:
    def __init__(self, file, app):
        with open(file, 'r') as stream:
            try:
                self.data = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)

        self.app = app
        self.ships = {}
        for ship in self.data['battle']['ships']:
            temp = Ship(ship)
            temp.attach(app)
            self.ships[temp.id] = temp

    def render_scene(self, turn):
        current_turn = self.data['battle']['turns'][turn]
        if turn != current_turn['time']:
            print("Turn does not match time!")
        for ship in current_turn['ships']:
            self.ships[ship['ship']].setPosition(ship['position'])

    def clear_scene(self):
        for key, ship in self.ships.items():
            ship.detach()
