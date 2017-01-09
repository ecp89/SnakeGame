from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from collections import deque
from kivy.graphics import Rectangle, Color
import operator

GAME_SPEED = 1.0/15.0




class Snake(Widget):
    SNAKE_SQAURE_SIZE = (9, 9)
    VELOCITY = 2
    SNAKE_COLOR = (1,0,0)


    def __init__(self, **kwargs):
        super(Snake, self).__init__(**kwargs)
        self.snake_body_prop = ListProperty([])
        self.snake_body = deque([])
        with self.canvas:
            Color(*Snake.SNAKE_COLOR)
            self.snake_body.append((Rectangle(pos=(200,200), size=(self.SNAKE_SQAURE_SIZE))))

        self.derive_property()

    def move(self, direction, last_direction):
        has_body = len(self.snake_body) > 1

        direction = last_direction if (has_body and ((direction[0] == last_direction[0]) or (direction[1] == last_direction[1]))) else direction
        rect = self.snake_body.pop() if has_body else self.snake_body[0]
        rect.pos = self.calculate_new_position(direction, self.snake_body[0].pos)
        self.snake_body.appendleft(rect) if has_body else None

        self.derive_property()
        return direction

    def calculate_new_position(self, direction, head_position):
        head_delta = map(operator.mul, self.SNAKE_SQAURE_SIZE, direction)
        new_head_pos = map(operator.add, head_delta, head_position)
        new_head_with_space = map(operator.add, new_head_pos, direction)
        return new_head_with_space

    def add_to_body(self):
        new_pos = map(operator.add, map(lambda x : x * -1, self.SNAKE_SQAURE_SIZE ) , self.snake_body[-1].pos)
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
    BORDER_WIDTH = 20
    last_direction = Vector(0, 0)
    # 273 -> up
    # 274 -> down
    # 275 -> right
    # 276 -> left
    keycodeToVector = {273: Vector(0,1), 274: Vector(0, -1), 275: Vector(1,0), 276: Vector(-1, 0)}
    snake = ObjectProperty(0)
    keypress = None

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
        with self.canvas:
            Color(1,1,1)
            Rectangle(pos=(0, 0), size=(SnakeGame.BORDER_WIDTH, Window.height))
            Rectangle(pos=(0, Window.height - SnakeGame.BORDER_WIDTH), size=(Window.width, SnakeGame.BORDER_WIDTH))
            Rectangle(pos=(Window.width - SnakeGame.BORDER_WIDTH, 0), size=(SnakeGame.BORDER_WIDTH, Window.height))
            Rectangle(pos=(0, 0), size=(Window.width, SnakeGame.BORDER_WIDTH))


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print('The key', keycode, 'have been pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        #self.update(0, keycode[0])
        self.keypress = keycode[0]
        return True

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def update(self, dt):
        current_direction = self.keycodeToVector.get(self.keypress, self.last_direction)
        self.last_direction = self.snake.move(current_direction, self.last_direction)
        if(self.keypress == 97): # 97 -> a
            self.snake.add_to_body()
        self.keypress = None

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, GAME_SPEED)
        return game


if __name__ == '__main__':
    SnakeApp().run()
