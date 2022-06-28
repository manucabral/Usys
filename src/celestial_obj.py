class CelestialObject:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Celestial Object')
        self.radius = kwargs.get('radius', 0)
        self.mass = kwargs.get('mass', 0)
        self.color = kwargs.get('color', 'white')
        self.category = kwargs.get('category', 'celestial object')

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'
