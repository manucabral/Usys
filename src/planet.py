from .celestial_obj import CelestialObject


class Planet(CelestialObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category = 'planet'
