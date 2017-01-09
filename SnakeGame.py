from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from collections import deque
from kivy.graphics import Rectangle
from kivy.graphics.instructions import InstructionGroup
import operator

GAME_SPEED = 1.0/10.0




class Snake(Widget):
    SNAKE_SQAURE_SIZE = (10, 10)
    START = (1,1)
    VELOCITY = 2
    SNAKE_SQUARE_SEP = 2

    #body = ListProperty([Rectangle(pos=(self.parent.center), size=(SNAKE_SQAURE_SIZE))])


    def __init__(self, **kwargs):
        super(Snake, self).__init__(**kwargs)
        self.snake_body_prop = ListProperty([])
        self.snake_body = deque([])
        with self.canvas:
            self.snake_body.append((Rectangle(pos=(200,200), size=(self.SNAKE_SQAURE_SIZE))))
            #new_pos = self.add_tuple((self.SNAKE_SQAURE_SIZE * -1), self.snake_body[-1].pos)
            self.snake_body.append((Rectangle(pos=(200,189), size=(self.SNAKE_SQAURE_SIZE))))
        # map(self.print_helper, self.snake_body)

        self.derive_property()
        # map(self.print_helper, self.snake_body_prop)

    def print_helper(self, r):
        print r.pos

    count = 401
    def move(self, direction):
        if direction != [0,0]:
            print("Length of snake_body_prop: {}".format(len(self.snake_body_prop)))
            if(len(self.snake_body) > 1):
                rect = self.snake_body.pop()
                rect.pos = map(operator.add, map(operator.add, map(operator.mul, self.SNAKE_SQAURE_SIZE, direction), self.snake_body[0].pos), map(operator.mul, (self.VELOCITY, self.VELOCITY), direction))
                self.snake_body.appendleft(rect)
            else:
                self.snake_body[0].pos = (direction*self.VELOCITY) + self.snake_body[0].pos

            self.derive_property()

    def add_to_body(self):
        new_pos = self.add_tuple(map(lambda x : x * -1, self.SNAKE_SQAURE_SIZE ) , self.snake_body[-1].pos)
        print("self.snake_body[-1].pos {}".format(self.snake_body[-1].pos))
        print(self.SNAKE_SQAURE_SIZE)
        print("new_pos {}".format(new_pos))
        with self.canvas:
            rec = Rectangle(pos=new_pos, size=self.SNAKE_SQAURE_SIZE)
            self.snake_body.append(rec)
        self.derive_property()

    def add_tuple(self, t1, t2):
        return (t1[0] + t2[0], t1[1] + t2[1])

    def derive_property(self):
        self.snake_body_prop = list(self.snake_body)


class SnakeGame(Widget):
    #snake = ObjectProperty(0)
    lastDir = Vector(0,0)
    # 273 -> up
    # 274 -> down
    # 275 -> right
    # 276 -> left
    keycodeToVector = {273: Vector(0,1), 274: Vector(0, -1), 275: Vector(1,0), 276: Vector(-1, 0)}
    snake = ObjectProperty(0)

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        # self.snake = Snake()

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
        if(keycode == 97):
            self.snake.add_to_body()

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, GAME_SPEED)
        return game


if __name__ == '__main__':
    SnakeApp().run()
