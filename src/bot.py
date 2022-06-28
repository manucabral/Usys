from .player import Player
from random import randint

PLANETS = ['Mercurio', 'Venus', 'Tierra', 'Marte',
           'Jupiter', 'Saturno', 'Urano', 'Neptuno', 'Pluton']


class Bot(Player):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', 'Bot')
        self.type = kwargs.get('type', 'bot')
        self.last_trys = []
        self.target = PLANETS

    def process(self):
        if len(self.last_trys) > 3:
            self.last_trys = []
            return 'take'
        for obj in self.objects:
            if obj.name in self.target:
                self.target.remove(obj.name)
        new_try = randint(0, len(self.target) -
                          1) if len(self.target) > 0 else -1
        if new_try != -1:
            self.last_trys.append(new_try)
        return self.target[new_try] if len(self.target) > 0 else 'take'
