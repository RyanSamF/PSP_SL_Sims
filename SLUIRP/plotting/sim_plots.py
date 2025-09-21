from matplotlib import *
import numpy as np
import matplotlib.pyplot as plt

def prof_graph(drift, alt, ws, angle, program, more = None):
    ################################################################################
    # Graphs horizontal position against vertical position, creating a profile of the flight
    # INPUTS:
    # drift - horizontal position/drift distance in feet (array)
    # alt - altitude in feet (array)
    # plt_title - Title of plot (usually x mph y Degrees RocketPy )
    # OUTPUTS:
    # None - displays plot and saves it
    ################################################################################
    fig, ax1 = plt.subplots()
    ax1.set_ylabel("Altitude (ft)")
    ax1.set_xlabel('Drift Distance (ft)')
    lns3 = ax1.plot(drift, alt, color=(0, 0, 1))
    plt.suptitle(program + " Flight Profile " + more if more != None else "",
        fontweight = 'bold')
    plot_name = str(ws)+" mph " + str(angle) + " Degrees"
    plt.title(plot_name)
    plt.grid()
    plt.savefig('Plots/' + plot_name + program + " Profile.png", format='png')

def param_graph(time, alt, vel, accel, ws, angle, program, more = None):
    ################################################################################
    # Graphs horizontal position against vertical position, creating a profile of the flight
    # INPUTS:
    # time - time array
    # alt - altitude in feet (array)
    # vel - vertical velocity of flight (array)
    # accel - vertical acceleration of flight (array)
    # ws - wind speed of flight in mph
    # angle - angle of flight in degrees
    # program - Program used to create data (usually "RocketPy" or "OpenRocket")
    # OUTPUTS:
    # plot_name - name of plot
    ################################################################################
    fig, ax1 = plt.subplots()
    plt.grid()
    ax1.set_ylabel("Altitude (ft)")
    ax1.set_xlabel('time (s)')
    lns3 = ax1.plot(time, alt, color=(0, 0, 1),label="Altitude")
    ax2 = ax1.twinx()
    ax2.set_ylabel('Acceleration (ft/s²), Velocity (ft/s)')
    lns1 = ax2.plot(time, accel, color=(0.9290, 0.6940, 0.1250), label="Acceleration")
    lns2 = ax2.plot(time, vel, color=(1,0,0), label="Velocity")
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc=0)
    ax1_ylims = ax1.axes.get_ylim()          
    ax1_yratio = ax1_ylims[0] / ax1_ylims[1]  

    ax2_ylims = ax2.axes.get_ylim()           
    ax2_yratio = ax2_ylims[0] / ax2_ylims[1] 
#COMMENT THIS
    if ax1_yratio < ax2_yratio: 
        ax2.set_ylim(bottom = ax2_ylims[1]*ax1_yratio)
    else:
        ax1.set_ylim(bottom = ax1_ylims[1]*ax2_yratio)
    plt.suptitle(program + " Flight Parameters vs. Time " + more if more != None else "" ,
                fontweight = 'bold')
    plot_name = str(ws)+" mph " + str(angle) + " Degrees"
    plt.xlim((0, time[-1]))
    plt.title(plot_name)
    
    plt.savefig('Plots/' + plot_name +  program + " Parameters.png", format='png')
    return(plot_name)