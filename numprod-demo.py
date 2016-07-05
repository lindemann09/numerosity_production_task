#!/usr/bin/python
"""
Example for the Numerosity Production Task

depends on Expyriment 0.7 or larger
"""

from expyriment import control, misc, stimuli
from numprod import NumerosityProductionTask


control.defaults.auto_create_subject_id = True
control.defaults.screen_open_gl = False # presentation is more fluent
                                        # if OpenGl is switched of
control.defaults.initialize_delay = 1 # please keep default value (10)
                         # in real experiment to ensure precise timing
#control.set_develop_mode(True)

exp = control.initialize()

npt = NumerosityProductionTask(experiment=exp,
        dot_radius = 8, area_radius = 300,
        dot_colour = (0, 255,0), # changing colours requires Expyriment 0.8
        background_colour = (0,0,0), gap = 2,
        more_key = misc.constants.K_UP,
        less_key = misc.constants.K_DOWN,
        enter_key = misc.constants.K_RETURN,
        use_mouse = True)


### start ###
control.start(exp)

stimuli.TextScreen(heading= "Numerosity Production Task",
                   text="Use mouse wheel or up/down keys to change numerosity.\n" +
                   "Press mouse button or ENTER to accept estimation.").present()
exp.keyboard.wait()
exp.data_variable_names = ["estimation", "latency"]

while True:

    # make numerosity production estimation
    estim, rt = npt.estimation(max_number = 100, start_value = 0,
                        scroll_out_direction = "E")
    # save data
    exp.data.add([estim, rt])


    stimuli.TextScreen(heading="The estimation was: {0}".format(estim),
                    text = "Another trial (y/n)").present()
    key, _ = exp.keyboard.wait([ord('y'), ord('n')])
    if key == ord('n'):
        break



control.end(goodbye_text="bye bye", goodbye_delay=5)
