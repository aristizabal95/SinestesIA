import numpy as np
def init():
    global g_current_state
    g_current_state = [0]*174
    global g_current_frame
    g_current_frame = np.zeros((128,128,1))
