# from snake.game import Game
# from snake.controller import KeyboardController
#
#
# if __name__ == '__main__':
#     game = Game(board_size=(5, 5), fps=1)
#     ctrl = KeyboardController()
#     with ctrl.run() as c:
#         game.start(c)
#
#     print(f"Final score: {game.get_score()}")

# KeyLogger_tk2.py
# show a character key when pressed without using Enter key
# hide the Tkinter GUI window, only console shows
import tkinter as tk


def key(event):
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.char == event.keysym:
        # normal number and letter characters
        print( 'Normal Key %r' % event.char )
    elif len(event.char) == 1:
        # charcters like []/.,><#$ also Return and ctrl/key
        print( 'Punctuation Key %r (%r)' % (event.keysym, event.char) )
    else:
        # f1 to f12, shift keys, caps lock, Home, End, Delete ...
        print( 'Special Key %r' % event.keysym )


if __name__ == '__main__':
    root = tk.Tk()
    print( "Press a key (Escape key to exit):" )
    root.bind_all('<Key>', key)
    # don't show the tk window
    # root.withdraw()
    root.mainloop()
    print("exited")
