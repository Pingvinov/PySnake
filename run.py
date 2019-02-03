from snake.game import Game
from snake.controller import KeyboardController


if __name__ == '__main__':
    game = Game(board_size=(5, 5), fps=1)
    ctrl = KeyboardController(buffersize=5)
    with ctrl.run() as c:
        game.start(c)

    print(f"Final score: {game.get_score()}")
