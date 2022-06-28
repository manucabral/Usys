class Player:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Player')
        self.objects = kwargs.get('objects', [])
        self.turn = False
        self.type = kwargs.get('type', 'player')

    def total_objects(self):
        return len(self.objects)

    def has_object(self, object_name):
        for obj in self.objects:
            if obj.name == object_name:
                return True
        return False

    def add_object(self, object):
        self.objects.append(object)

    def remove_object(self, object_name):
        for obj in self.objects:
            if obj.name == object_name:
                self.objects.remove(obj)
                return obj
        return False
