#!/usr/bin/python

# depends on Expyriment 0.7

from expyriment import control, misc, stimuli
import expyriment.stimuli.extras
from numprod import np_estimate, scroll_out

control.defaults.screen_open_gl = False
control.defaults.initialize_delay = 1
control.defaults.auto_create_subject_id = True
#control.set_develop_mode(True)

exp = control.initialize()
control.start(exp)

estim, rt = np_estimate(experiment=exp,
        max_number = 100,
        start_value = 0,
        dot_radius = 8,
        area_radius = 300,
        dot_colour = (0, 255,0), # changing colours requires Expyriment 0.8
        background_colour = (0,0,0),
        gap = 2,
        more_key = misc.constants.K_UP,
        less_key = misc.constants.K_DOWN,
        enter_key = misc.constants.K_RETURN,
        use_mouse = False,
        scroll_out_direction = "E")
print estim, rt

control.end(goodbye_text="bye bye", goodbye_delay=1000),
