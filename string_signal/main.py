# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:44:19 2015

@author: ryuhei
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import vrep

def draw_lrf(lrf):
    lrf = np.asarray(lrf)
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.plot(0, 0, 'r>', markersize=10)
    ax.scatter(lrf[:, 0], lrf[:, 1])
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.grid()
    plt.show()

if __name__ == '__main__':
    try:
        client_id
    except NameError:
        client_id = -1
    e = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot_wait)
    vrep.simxFinish(-1)
    client_id = vrep.simxStart('127.0.0.1', 19998, True, True, 5000, 5)

    assert client_id != -1, 'Failed connecting to remote API server'

    e = vrep.simxStartSimulation(client_id, vrep.simx_opmode_oneshot_wait)

    # print ping time
    sec, msec = vrep.simxGetPingTime(client_id)
    print "Ping time: %f" % (sec + msec / 1000.0)

    name_hokuyo_data = "hokuyo_data"
    vrep.simxGetStringSignal(client_id, name_hokuyo_data,
                             vrep.simx_opmode_streaming)

    num_steps = 1000
    for t in range(num_steps):
        e, lrf_bin = vrep.simxGetStringSignal(client_id, name_hokuyo_data,
                                              vrep.simx_opmode_buffer)
        lrf_raw = vrep.simxUnpackFloats(lrf_bin)
        lrf = np.array(lrf_raw).reshape(-1, 3)

        print "step {}".format(t)
#        print lrf
        draw_lrf(lrf)

    e = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot_wait)
