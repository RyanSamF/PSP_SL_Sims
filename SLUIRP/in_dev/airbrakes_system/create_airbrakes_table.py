import pandas as pd
from SLUIRP.in_dev.airbrakes_system.altitude_optimization import alt_opt
import numpy as np

"""
create_airbrakes_table()
4) use function 3 to create lookup table of needed Cd values given mach number, current altitude, desired altitude
    INPUT:
    Array of Input velocities/mach
    Array of input heights
    Array of input angles
    Desired height
"""

def airbrakes_table(init_vels, init_alts, init_angles, apogee, vehicle_file, drag_data):
    data = np.zeros((len(init_vels), len(init_alts)))
    angle_dict = {}
    for angle_index in range(len(init_angles)):
        for v_index in range(len(init_vels)):
            for alt_index in range(len(init_alts)):
                data[v_index, alt_index] = alt_opt(vehicle_data=vehicle_file,
                                                                init_vel=init_vels[v_index],
                                                                init_angle=init_angles[angle_index],
                                                                init_alt=init_alts[alt_index],
                                                                goal_alt=apogee,
                                                                drag_file=drag_data)
        labelled_data = pd.DataFrame(data, index=init_vels, columns=init_alts)
        angle_dict[init_angles[angle_index]] = labelled_data
        print(labelled_data)
