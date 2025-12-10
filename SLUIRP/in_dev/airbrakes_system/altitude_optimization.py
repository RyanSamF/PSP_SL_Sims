"""
alt_optimize()
Get Cd value at starting mach number and starting altitude to reach desired altitude
    INPUT:
        Starting mach number
        Rocket data
        Starting altitude
        Starting angle
        Desired altitude

        Function 3 output
    OUTPUT: CD value to reach desired altitude

    1) run function 1 with input CD value (probably 0% deployment)
    2) Look at output of function 1 and adjust CD value input based on difference in height 
    3) Repeat 1 and 2 until output altitude = desired altitude (while loop)
"""
import math
import numpy as np
from SLUIRP.in_dev.airbrakes_system.midair_sims import midair_sim
from SLUIRP.in_dev.airbrakes_system.CD_slope_estimation import CD_curve_estimate
from SLUIRP.data.OpenYAML import readYaml

def cd_equation (init_vel, velocity, cd):

    return cd
def alt_opt(vehicle_data, init_vel, init_angle, init_alt, goal_alt, drag_file):
    init_drag = 0.5 #vehicle.power_off_drag(init_vel / 343)
    cur_drag = init_drag
    #print(init_drag)
    #print(cur_drag)
    #mach_curve, cd_curve = CD_curve_estimate(drag_file, init_vel / 343, init_drag)
    cur_apogee = midair_sim(vehicle_data, init_vel, init_alt,init_angle, drag_data = cur_drag) #np.column_stack([mach_curve, cd_curve]))
    #print(np.abs(cur_apogee - goal_alt))
    n = 0
    while np.abs(cur_apogee - goal_alt) > goal_alt / 1000:
        n += 1
        cur_drag = cur_drag - (goal_alt - cur_apogee) / (500 + 10*n)
        #print(cur_drag, end='\r')
        #print("drag:", cur_drag)
        #mach_curve, cd_curve = CD_curve_estimate(drag_file, init_vel / 343, cur_drag)
        cur_apogee = midair_sim(vehicle_data, init_vel, init_alt,init_angle, drag_data = cur_drag) #np.column_stack([mach_curve, cd_curve]))
        #print("Apogee:", cur_apogee)
        if cur_drag < 0.1 and cur_apogee < goal_alt:
            return(-1)
        if cur_drag > 0.7 and cur_apogee > goal_alt:
            return(-2)
    if cur_drag > 0.1 and cur_drag < 0.7:
        return(cur_drag)
    elif cur_drag < 0.1:
        return(-1)
    else:
        return(-2)

