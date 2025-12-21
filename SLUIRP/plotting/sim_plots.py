from matplotlib import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import folium

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
    plt.suptitle(program + " Flight Profile " + more if more != None else program + " Flight Profile",
        fontweight = 'bold')
    plot_name = str(ws)+" mph " + str(angle) + " Degrees"
    plt.title(plot_name)
    plt.grid()
    plt.savefig('Plots/' + plot_name + program + " Profile.png", format='png')

def param_graph(time, alt, vel, accel, ws, angle, program, more = None, ejections = None):
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
    if ejections is not None:
        #Places vertical lines at drogue and main deployment, and attempts to place labels where readable
        #Currently places labels above where altitude is at main deployment so drogue label is below ascent parabola
        # and main label is above main descent
        plt.axvline(x=ejections[0], color='black', linestyle='--', label='Drogue Deployment')
        plt.text(x=ejections[0] + time[-1]*0.01, y=alt[ejections[1]] * 1.02, s='Drogue Deployment',rotation=90, color ='black')
        plt.axvline(x=ejections[1], color='black', linestyle='--', label='Main Deployment')
        plt.text(x=ejections[1] + time[-1]*0.01, y=alt[ejections[1]] * 1.02, s='Main Deployment',rotation=90, color='black')
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
    plt.suptitle(program + " Flight Parameters vs. Time " + more if more != None else program + " Flight Parameters vs. Time" ,
                fontweight = 'bold')
    plot_name = str(ws)+" mph " + str(angle) + " Degrees"
    plt.xlim((0, time[-1]))
    plt.title(plot_name)
    
    plt.savefig('Plots/' + plot_name +  program + " Parameters.png", format='png')
    return(plot_name)

def drift_map(drifts, wind_speeds, max_drift, program = None):
    img_path = 'SLUIRP/plotting/raw_map.jpg'
    img = plt.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img, zorder=0, extent=[-3000, 3000, -3000, 3000], aspect=1)
    inner_radii = [0] + drifts[:-1]
    # Iterate through the radii to draw rings
    for i, r_outer in enumerate(drifts):
        r_inner = inner_radii[i]
        
        # Calculate the width of the current ring
        width = r_outer - r_inner

        # Get color for wedge
        percent = r_outer/max_drift
        print(percent)
        if percent < 0.5:
            color = (min(1,percent*2), 1, 0)
        else:
            color = (1, min(1,1-(percent-0.5)*2), 0)
        # Create a Wedge (full ring since theta1=0, theta2=360)
        # We set the inner radius as r_inner and outer as r_outer with the correct width
        # The width parameter of Wedge defines the radial width of the wedge
        ring = patches.Wedge(
            (0, 0), 
            r_outer, 
            theta1=0, 
            theta2=360, 
            width=width,
            facecolor=color,
            alpha = 0.5,
            edgecolor='none', # Avoid double-drawing edges which can cause overlap artifacts
            label = str(wind_speeds[i]) + " MPH"
        )
        ax.add_patch(ring)
        #plt.text(x=0, y=r_inner + width/2,  s=str(wind_speeds[i]) + " MPH",horizontalalignment='center', color="white")
    ring = patches.Wedge(
            (0, 0), 
            max_drift, 
            theta1=0, 
            theta2=360, 
            width=max_drift-max(drifts),
            facecolor=(1,0,0),
            alpha=0.5,
            edgecolor='none', # Avoid double-drawing edges which can cause overlap artifacts
            label = "Max Drift Allowed"
        )
    ax.add_patch(ring)
    #plt.text(x=0,y=max(drifts) + (max_drift-max(drifts))/2, s="Max Drift Allowed", horizontalalignment='center',color = "white")
    ax.scatter(0,0, color='red', label = "Launch Site")
    plt.xlabel("East/West Distance from Launch")
    plt.ylabel("North/South Distance from Launch")
    plt.suptitle("Wind Speed vs. Drift Distance Map", fontweight='bold')
    plt.title(program)
    plt.legend()
    plt.show()

drift_map([408.38, 984.43, 1463.25, 1903.15],[5, 10, 15, 20], 2500, "OpenRocket")