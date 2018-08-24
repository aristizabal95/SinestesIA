import numpy as np
def init():
    global g_current_state
    g_current_state = []
    global g_current_frame
    g_current_frame = np.zeros((240,320,4))
