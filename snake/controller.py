import tkinter as tk
from contextlib import contextmanager


class Controller(object):

    def start(self):
        pass

    def end(self):
        pass

    @contextmanager
    def run(self):
        self.start()
        yield
        self.end()

    def receive_input(self):
        return None

    def send_output(self, board_state):
        return None


class KeyboardController(Controller):
    def __init__(self):
        self._event_handler = tk.Tk()

    def _get_key(self, event):
        """shows key or tk code for the key"""
        if event.keysym == 'Escape':
            self.end()
        if event.char == event.keysym:
            # normal number and letter characters
            print('Normal Key %r' % event.char)
        elif len(event.char) == 1:
            # charcters like []/.,><#$ also Return and ctrl/key
            print('Punctuation Key %r (%r)' % (event.keysym, event.char))
        else:
            # f1 to f12, shift keys, caps lock, Home, End, Delete ...
            print('Special Key %r' % event.keysym)

    def start(self):
        print("Controller started. Press Esc to exit.")
        self._event_handler.bind_all('<Key>', self._get_key)
        self._event_handler.mainloop()

    def end(self):
        self._event_handler.destroy()

    def receive_input(self):
        pass