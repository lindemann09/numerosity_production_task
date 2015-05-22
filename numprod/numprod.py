"""Numerosity production

(c) 2010-2015 Oliver Lindemann

"""

import time
from expyriment import io, misc
from expyriment.stimuli.extras import DotCloud
from animation import scroll_out

def np_estimate(experiment,
             max_number,
             start_value = 0,
             area_radius = 300,
             dot_radius = 8,
             dot_colour = (0,255,0),
             background_colour = (0,0,0),
             gap = 2,
             more_key = misc.constants.K_UP,
             less_key = misc.constants.K_DOWN,
             enter_key = misc.constants.K_RETURN,
             use_mouse = False,
             scroll_out_direction = None):
    """
    scroll_out_direction must be "S", "N", "E" or "W"
    """

    dc = NumerosityProduction(radius=area_radius,
                        dot_colour=dot_colour,
                        background_colour=background_colour)
    dc.make(max_number=max_number, dot_radius=dot_radius, gap=gap)

    dc.present()
    experiment.clock.reset_stopwatch()
    if use_mouse:
        mouse = io.Mouse(show_cursor=True, track_button_events=True)
    else:
        mouse = None

    m = None
    while (True):
        k = experiment.keyboard.check()
        if use_mouse:
            m = mouse.get_last_button_down_event()

        if k == more_key or m == 4:
            dc.increase()
            dc.present()
        elif k == less_key or m == 5:
            dc.decrease()
            dc.present()
        elif k == enter_key or m == 1 :
            break
        time.sleep(0.01)

    rt = experiment.clock.stopwatch_time

    if scroll_out_direction is not None:
        scroll_out(experiment, dc, scroll_out_direction)

    return dc.number_of_presented_dots, rt


class NumerosityProduction(DotCloud):

    def __init__(self, radius=None, position=None, background_colour=None,
                       dot_colour=None):
        DotCloud.__init__(self, radius=radius, position=position,
                    background_colour=background_colour, dot_colour=dot_colour)
        self.set_logging(False)
        self._full_cloud = DotCloud(radius=radius, position=position,
                    background_colour=background_colour, dot_colour=dot_colour)
        self._full_cloud.set_logging(False)
        self._n_dots = 0

    def make(self, max_number, dot_radius, gap=0):
        """see docu DotCloud.make """
        self._full_cloud.make(n_dots=max_number, dot_radius=dot_radius)
        self.clear_surface()

    @property
    def max_number(self):
        return len(self._full_cloud._cloud)

    @property
    def number_of_presented_dots(self):
        return self._n_dots

    def shuffel_dot_sequence(self, from_idx=0, to_idx= -1):
        """see Exypriment docu DotCloud.shuffel_dot_sequence"""
        self._full_cloud.shuffel_dot_sequence(from_idx, to_idx)
        self._set_cloud()

    def _set_cloud(self):
        self._cloud = self._full_cloud._cloud[:self._n_dots]
        self.create_area()
        self.clear_surface()

    def shuffel_not_visual_dots(self):
        self._full_cloud.shuffel_dot_sequence(
                    from_idx=self._n_dots,
                    to_idx=-1)

    def increase(self):
        self._n_dots += 1
        if self._n_dots > self.max_number:
            self._n_dots = self.max_number
        else:
            self._set_cloud()

    def decrease(self):
        self._n_dots -= 1
        if self._n_dots < 0:
            self._n_dots = 0
        else:
            self._set_cloud()
            self.shuffel_not_visual_dots()

