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
from midair_sims.py import midair_sim(vehicle, init_vel, init_alt, init_angle)
from CD_slope_estimation.py import #NAME (cd_file, velocity, cd)
def cd_equation (init_vel, velocity, cd):

    return cd
def alt_opt (init_vel, init_angle, init_apogee):
    area = math.pi*((diameter**2)/4)
    force_drag = 0.5*(init_vel**2)*1.204*area
    return
apogee = 4750
while actual_apogee != apogee:
    if actual_apogee < apogee:
        cd_test = (cd_min + cd)/2
        actual_apogee = alt_opt(init_vel, init_angle, init_apogee)
    elif actual_apogee > apogee:
        cd_test = (cd_max + cd)/2
        actual_apogee = alt_opt(init_vel, init_angle, init_apogee)