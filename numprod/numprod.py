"""Numerosity production task

This file part of the numprod
See LICENCE file distributed with the package

"""

import time
from expyriment import io, misc
from expyriment.stimuli.extras import DotCloud
from animation import scroll_out

class NumerosityProductionTask(object):

    def __init__(self, experiment,
             area_radius = 300,
             dot_radius = 8,
             dot_colour = (0,255,0),
             background_colour = (0,0,0),
             gap = 2,
             more_key = misc.constants.K_UP,
             less_key = misc.constants.K_DOWN,
             enter_key = misc.constants.K_RETURN,
             use_mouse = False):

        """Numerosity Production Task

        Parameters
        ----------
        experiment : Expyriment experiment
            the currently running experiment
        area_radius : integer, optional
            radius of the area in which the dots will appear
        background_colour : Expyriment colour
            background colour of the area in which the will appear
        dot_radius : integer, optional
            radius of a single dot
        dot_colour : Expyriment colour, optional
            colour of the dots
        gap : integer, optional
            minimum space between two dots
        more_key : integer, key code, optional
            key event that increases the number of dots
        less_key : integer, key code, optional
            key event that decreases the number of dots
        enter_key : integer, key code, optional
            key event that quits the numerosity production
        use_mouse : boolean, optional
            if true dot cloud can be control via the mouse wheel, mouse
            click quits quits the numerosity production

        """

        self.cloud = NumerosityProductionCloud(radius=area_radius,
                        dot_colour=dot_colour,
                        background_colour=background_colour)

        self.gap = gap
        self.dot_radius = dot_radius
        self.clock = misc.Clock()
        self.experiment = experiment
        if use_mouse:
            self._mouse = io.Mouse(show_cursor=True, track_button_events=True)
        else:
            self._mouse = None
        self._control_key ={"more": more_key, "less":less_key, "enter":enter_key}

    def estimation(self, max_number,
             start_value = 0,
             scroll_out_direction = None):
        """Make a numerosity production estimation

        Parameters
        ----------
        max_number : integer
            maximum number of dots that can be produced
        start_value : integer, optional
            number of dots to starts with
        scroll_out_direction : direction char, optional
            if this parameter is set to "E", "W", "N" or "S" the dot pattern move
            out of the screen after the numerosity production has been quitted.
            Letters indicate the cardinal movement directions east, west, north
            or south.

        Returns
        -------
        estimate : integer
            produced number of dots
        rt : integer
            latencies (in ms) between the start of the function and the time
            the estimation has been be quitted.
        """

        self.cloud.make(max_number=max_number, dot_radius=self.dot_radius,
                        start_value=start_value, gap=self.gap)

        self.cloud.present()
        self.clock.reset_stopwatch()
        m = None
        while (True):
            k = self.experiment.keyboard.check()
            if self._mouse is not None:
                m = self._mouse.get_last_button_down_event()

            if k == self._control_key["more"]or m == 3:
                self.cloud.increase()
                self.cloud.present()
            elif k == self._control_key["less"] or m == 4:
                self.cloud.decrease()
                self.cloud.present()
            elif k == self._control_key["enter"] or m == 1 :
                break
            time.sleep(0.01)

        rt = self.clock.stopwatch_time

        if scroll_out_direction is not None:
            scroll_out(self.experiment, self.cloud, scroll_out_direction,
                       pixel_per_ms = 1, reset_position=True)

        return self.cloud.number_of_presented_dots, rt


class NumerosityProductionCloud(DotCloud):
    """Child of dot cloud.

    A full dot pattern will be created but only part of the dots will be
    shown. With increase and decrease method the number of presented dots
    can be changed, Invisible dots will be shuffled after increase to
    ensure non-predictive appearance of dots.

    """

    def __init__(self, radius=None, position=None, background_colour=None,
                       dot_colour=None):
        DotCloud.__init__(self, radius=radius, position=position,
                    background_colour=background_colour, dot_colour=dot_colour)
        self.set_logging(False)
        self._full_cloud = DotCloud(radius=self.radius, position=self.position,
                    background_colour=self.background_colour, dot_colour=self.dot_colour)
        self._full_cloud.set_logging(False)
        self._n_dots = 0


    def make(self, max_number, dot_radius, start_value=0, gap=0):
        """Crete the dot cloud. see also docu DotCloud.make

        Parameters
        ----------
        max_number : integer
            maximum number of dots that can be produced
        dot_radius : integer
            radius of a single dot
        start_value : integer, optional
            number of dots to starts with
        gap : integer, optional
            minimum space between two dots

        """

        self._full_cloud.make(n_dots=max_number, dot_radius=dot_radius) # new randomization
        self._n_dots = start_value
        self._set_cloud()

    @property
    def max_number(self):
        return len(self._full_cloud._cloud)

    @property
    def number_of_presented_dots(self):
        return self._n_dots

    def shuffle_dot_sequence(self, from_idx=0, to_idx= -1):
        """see Exypriment docu DotCloud.shuffle_dot_sequence"""
        self._full_cloud.shuffel_dot_sequence(from_idx,
                            to_idx) # deprecated Expyriment 0.7 method
        self._set_cloud()

    def _set_cloud(self):
        self._cloud = self._full_cloud._cloud[:self._n_dots]
        self.create_area()
        self.clear_surface()

    def shuffle_invisible_dots(self):
        self._full_cloud.shuffel_dot_sequence(
                    from_idx=self._n_dots,
                    to_idx=-1) # deprecated Expyriment 0.7 method

    def increase(self):
        """increase the number of presented dots"""

        self._n_dots += 1
        if self._n_dots > self.max_number:
            self._n_dots = self.max_number
        else:
            self._set_cloud()

    def decrease(self):
        """decrease the number of presented dots"""
        self._n_dots -= 1
        if self._n_dots < 0:
            self._n_dots = 0
        else:
            self._set_cloud()
            self.shuffle_invisible_dots()
