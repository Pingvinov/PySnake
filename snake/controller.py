import tkinter as tk
import serial

from contextlib import contextmanager
from collections import deque

from snake.extras import Actions


class Controller(object):

    def start(self):
        pass

    def end(self):
        pass

    @contextmanager
    def run(self):
        self.start()
        yield self
        self.end()

    def receive_input(self):
        return None

    def send_output(self, board_state):
        return None


class KeyboardController(Controller):
    def __init__(self, keymap=None, buffersize=1, port='COM1'):
        self._keymap = keymap or {'quit': 'q', 'pause': 'p'}
        self._event_buffer = deque(maxlen=buffersize)
        self._event_handler = tk.Tk()
        self._prev_action = Actions.HALT
        try:
            self._serial_connection = serial.Serial(port, baudrate=9600, timeout=0.1)
        except:
            print("Cannot connect to the board.")
            self._serial_connection = None

    def _get_key(self, event):
        if event.keysym == self._keymap['quit']:
            self.end()
        elif event.keysym == self._keymap['pause']:
            self._event_buffer.clear()
            self._prev_action = Actions.HALT
        elif event.keysym in {'Up', 'Down', 'Left', 'Right'}:
            self._event_buffer.append(getattr(Actions, event.keysym.upper()))
        else:
            print(f"Undefined action for key {event.keysym}")

    def start(self):
        self._event_handler.bind_all('<Key>', self._get_key)
        self._event_handler.mainloop()

    def end(self):
        self._event_handler.destroy()

    def receive_input(self):
        if len(self._event_buffer) > 0:
            action = self._event_buffer.popleft()
            self._prev_action = action
            return action
        return self._prev_action

    def send_output(self, board_state):
        if self._serial_connection is not None:
            flattened_state = sum([s.rgb for s in board_state], ())
            for s in flattened_state:
                self._serial_connection.write(s)

