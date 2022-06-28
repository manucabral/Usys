

class Scene:
    def __init__(self, **kwargs):
        self.info = kwargs.get('info', 'Scene')
        self.options = kwargs.get('options', [])
        self.title = kwargs.get('title', 'USYS')

    def max_options(self):
        return len(self.options)

    def draw(self, options=True):
        print(self.info)
        if options:
            for index, option in enumerate(self.options):
                print(f'{index}: {option.text}')
