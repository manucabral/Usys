from .celestial_obj import CelestialObject


class Star(CelestialObject):
    def __init__(self, **kwargs):
        self.category = 'star'
        super().__init__(**kwargs)
