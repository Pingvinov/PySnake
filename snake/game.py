import time

from snake.environment import Environment
from snake.extras import Actions, GameState


class Game:
    def __init__(self, board_size, fps=1):
        self.environment = Environment(board_size)
        self._fps = fps

    def quit(self):
        pass

    def start(self, crtl):
        gs = GameState.IN_PROGRESS
        while gs == GameState.IN_PROGRESS:
            t_begin = time.time()
            action = crtl.receive_input()
            if action != Actions.HALT:
                gs, _ = self.environment.update_state(action)
            crtl.send_output(board_state=self.environment.state)
            t_end = time.time()
            time.sleep(max(0., 1.0 / self._fps - (t_end - t_begin)))
        if gs == GameState.WIN:
            self.show_win()
        elif gs == GameState.LOSS:
            self.show_lost()
        self.quit()

    def show_win(self):
        pass

    def show_lost(self):
        pass

    def get_score(self):
        return self.environment.score
