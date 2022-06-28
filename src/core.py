import colorama
from colorama import Fore, Back, Style
from os import system
from time import sleep
from cornelius import Keyboard
from random import randint

from .player import Player
from .bot import Bot
from .scene import Scene
from .option import Option
from .planet import Planet

Planets = [
    Planet(name='Mercurio', color=Fore.RED, radius=1, mass=1),
    Planet(name='Venus', color=Fore.YELLOW, radius=1, mass=1),
    Planet(name='Tierra', color=Fore.GREEN, radius=1, mass=1),
    Planet(name='Marte', color=Fore.LIGHTRED_EX, radius=1, mass=1),
    Planet(name='Jupiter', color=Fore.MAGENTA, radius=1, mass=1),
    Planet(name='Saturno', color=Fore.CYAN, radius=1, mass=1),
    Planet(name='Urano', color=Fore.WHITE, radius=1, mass=1),
    Planet(name='Neptuno', color=Fore.BLUE, radius=1, mass=1),
    Planet(name='Pluton', color=Fore.LIGHTBLUE_EX, radius=1, mass=1),
]


class Core:
    running = False
    current_scene = 'MENU'
    scenes = {}
    selector = 0
    keyboard = Keyboard()
    player = bot = None

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', 'USYS')
        self.version = kwargs.get('version', '0.0.0')
        self.author = kwargs.get('author', 'Anonymous')

    def init(self):
        colorama.init(autoreset=True)
        self.running = True
        system('cls')
        system('title ' + self.title)

        self.scenes['MENU'] = Scene(
            title='Menu',
            info='Menu principal',
            options=[
                Option(text='Nueva partida', action=self.new_match, args=None),
                Option(text='Salir', action=self.quit, args=None),
            ]
        )
        self.scenes['MATCH'] = Scene(
            title='Partida',
            info='Nueva partida',
            options=[
                Option(text='Intentar robar objeto', action=self.steal_object),
                Option(text='Agarrar nuevo objeto',
                       action=self.take_object),
                Option(text='Salir', action=self.quit_to_menu),
            ]
        )

    def toggle_turn(self):
        self.player.turn = not self.player.turn
        self.bot.turn = not self.bot.turn

    def steal_object(self):
        while True:
            system('cls')
            for index, obj in enumerate(Planets):
                print(f'{index} - {obj.color}{obj.name}{Fore.RESET}')
            print(
                f'{Fore.YELLOW}Selecciona un planeta para robarle al bot{Fore.RESET}')
            value = int(input())
            if value in range(len(Planets)):
                target_object = Planets[value]
                if self.bot.has_object(target_object.name):
                    self.player.add_object(target_object)
                    self.bot.remove_object(target_object.name)
                    print(
                        f'{Fore.YELLOW}Le robaste {target_object.color}{target_object.name}{Fore.YELLOW} al bot{Fore.RESET}!')
                else:
                    print(
                        f'{Fore.RED}Oh no! El bot no tiene ese objeto{Fore.RESET}')
                    new_object = self.take_object()
                    self.player.add_object(new_object)
                break
            sleep(4)
            self.toggle_turn()

        sleep(1)
        self.toggle_turn()

    def take_object(self):
        return Planets[randint(0, len(Planets) - 1)]

    def new_match(self):
        self.current_scene = 'MATCH'
        print(f'{Fore.YELLOW}Preparando nueva partida ..{Fore.RESET}')
        self.player = Player()
        for _ in range(4):
            self.player.add_object(self.take_object())
        sleep(1)
        print(f'{Fore.YELLOW}Preparando bot{Fore.RESET} ..')
        self.bot = Bot()
        for _ in range(4):
            self.bot.add_object(self.take_object())
        sleep(1)
        print(f'{Fore.YELLOW}Partida iniciada{Fore.RESET}')
        self.player.turn = True

    def update(self):
        system('cls')
        current = self.scenes[self.current_scene]
        if self.current_scene == 'MATCH':
            current.info = f'{Fore.YELLOW}Partida en curso, intenta conseguir todos los\nplanetas del sistema solar antes que el bot!\n\n{Fore.RESET}'
            current.info += f'{Fore.LIGHTYELLOW_EX}Tus objetos astronomicos{Fore.RESET} ({self.player.total_objects()})\n> '
            for obj in self.player.objects:
                current.info += f'{obj.color}{obj.name}{Fore.RESET} '
            current.info += '\n\n'
            current.info += f'{Fore.LIGHTYELLOW_EX}Objetos del bot{Fore.RESET} ({self.bot.total_objects()})\n\n'
            current.info += f'> {Fore.LIGHTWHITE_EX}{"Tu turno" if self.player.turn else "Turno del bot"}{Fore.RESET}'

        current.draw(self.player.turn if self.current_scene ==
                     'MATCH' else True)

    def handle_input(self):
        if self.current_scene == 'MATCH' and self.bot.turn:
            print(f'{Fore.LIGHTYELLOW_EX}Bot pensando {Fore.RESET}..')
            object_selected_name = self.bot.process()
            print('Bot proceso:', object_selected_name)
            if object_selected_name == 'take':
                self.bot.add_object(self.take_object())
                print(f'{Fore.LIGHTYELLOW_EX}Bot agarró un objeto{Fore.RESET}')
            elif self.player.has_object(object_selected_name):
                removed_object = self.player.remove_object(
                    object_selected_name)
                self.bot.add_object(removed_object)
                print(
                    f'{Fore.YELLOW}El bot te ha robado a {removed_object.color}{removed_object.name}{Fore.RESET}!')
            else:
                selected_obj = None
                for obj in Planets:
                    if obj.name == object_selected_name:
                        selected_object = obj
                print(
                    f'{Fore.LIGHTYELLOW_EX}El bot intento robarte a {selected_object.color}{selected_object.name}{Fore.RESET}!')
            total = 0
            for planet in Planets:
                if planet in self.bot.objects:
                    total += 1
            if total == len(Planets):
                print(
                    f'{Fore.LIGHTYELLOW_EX}El bot ha conseguido todos los planetas{Fore.RESET}')
                self.quit()
            sleep(4)
            self.toggle_turn()

        else:
            while True:
                value = int(input())
                if value < 0 or value > self.scenes[self.current_scene].max_options():
                    sleep(0.5)
                    self.update()
                    continue
                else:
                    self.selector = value
                    break
            option = self.scenes[self.current_scene].options[self.selector]
            option.execute()

    def quit(self):
        self.running = False

    def quit_to_menu(self):
        self.current_scene = 'MENU'
        self.selector = 0

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.handle_input()
