class Option:
    def __init__(self, **kwargs):
        self.text = kwargs.get('text', 'Option')
        self.callback = kwargs.get('action', lambda: None)

    def execute(self, args=None):
        if args is None:
            return self.callback()
        return self.callback(*args)
