from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window


class Snake(Widget):
    START = (1,1)
    body = ListProperty([Vector(START)])


    def move(self, direction):
        if(direction):
            self.pos = direction + self.pos



class SnakeGame(Widget):
    snake = ObjectProperty(0)
    lastDir = None
    keycodeToVector = {273: Vector(0,1), 274: Vector(0, -1), 275: Vector(1,0), 276: Vector(-1, 0)}

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        self.update(0, keycode[0])
        return True

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def update(self, dt, keycode=None):
        self.lastDir = self.keycodeToVector.get(keycode, self.lastDir)
        self.snake.move(self.lastDir)


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game


if __name__ == '__main__':
    SnakeApp().run()
