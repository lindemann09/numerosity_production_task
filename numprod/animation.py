"""
Scroll stimuli out of the screen

(c) Oliver Lindemann

"""

import time
from expyriment import control, stimuli, misc
from expyriment.misc.geometry import XYPoint

control.defaults.open_gl = False

directions = ["N", "E", "S", "W"]

class StepTimer():

    def __init__(self, pixel_per_ms, direction):
        self.direction = direction
        self.pixel_per_ms = pixel_per_ms
        self._clock = misc.Clock()

    def reset_timer(self):
        self._clock.reset_stopwatch()

    def step(self):
        while True:
            step_size = int(self.pixel_per_ms * self._clock.stopwatch_time)
            if step_size == 0:
                # slow down if called to frequently
                time.sleep(0.001)
            else:
                break
        self._clock.reset_stopwatch()

        if self.direction == "N":
            return (0, step_size)
        elif self.direction == "W":
            return (-1*step_size, 0)
        elif self.direction == "S":
            return (0, -1*step_size)
        elif self.direction == "E":
            return (step_size, 0)

        return None

def _movement_end_position(direction, screen_size, stimulus):
    # define positions N, S, W, E
    if direction =="N":
        return (stimulus.position[0],
               (screen_size[1]/2 + stimulus.surface_size[1]/2 +1))
    elif direction == "E":
        return ((screen_size[0]/2 + stimulus.surface_size[0]/2 +1),
                stimulus.position[1])
    elif direction == "S":
        return (stimulus.position[0],
                -1*(screen_size[1]/2 + stimulus.surface_size[1]/2 +1))
    elif direction == "W":
        return (-1*(screen_size[0]/2 + stimulus.surface_size[0]/2 +1),
                stimulus.position[1])
    raise RuntimeError("Known movement direction. Direction must be " +
                     "'N', 'S', 'W' or 'E'")


def scroll_out(experiment, stimulus, movement_direction, pixel_per_ms = 0.5):
    """Scroll stimulus out of the screen

    movement direction must be "S", "N", "E" or "W"

    """

    stim_size = stimulus.surface_size
    end_pos = XYPoint(_movement_end_position(movement_direction,
                        experiment.screen.size, stimulus))
    # animate
    last_distance = 99999
    st = StepTimer(pixel_per_ms = pixel_per_ms,
                    direction = movement_direction)

    stop_motion = False
    while not(stop_motion):
        clear_box = stimuli.Rectangle(size=stim_size,
                    position = stimulus.position,
                    colour = experiment.background_colour)
        clear_box.set_logging(False)
        clear_box.present(update=False, clear=False)

        stimulus.move(st.step())
        distance = XYPoint(stimulus.position).distance(end_pos)
        if distance > last_distance:
            # move to end_pos and show once
            stop_motion = True
            stimulus.move((end_pos.x - stimulus.position[0],
                           end_pos.y - stimulus.position[1]))
        stimulus.present(update=False, clear=False)
        experiment.screen.update_stimuli([clear_box, stimulus])
        last_distance = distance
