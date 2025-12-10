import pandas as pd
from SLUIRP.in_dev.airbrakes_system.altitude_optimization import alt_opt
import numpy as np
import scipy
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


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
        cur_angle = init_angles[angle_index]
        for v_index in range(len(init_vels)):
            cur_vel = init_vels[v_index]
            for alt_index in range(len(init_alts)):
                cur_alt = init_alts[alt_index]
                data[v_index, alt_index] = alt_opt(vehicle_data=vehicle_file,
                                                                init_vel=cur_vel,
                                                                init_angle=cur_angle,
                                                                init_alt=cur_alt,
                                                                goal_alt=apogee,
                                                                drag_file=drag_data)
                print(alt_index+len(init_alts)*v_index+len(init_alts)*len(init_vels)*angle_index, end = "\r")
        labelled_data = pd.DataFrame(data, index=init_vels, columns=init_alts)
        angle_dict[init_angles[angle_index]] = labelled_data
        print(labelled_data)
        labelled_data.to_csv('lookup'+str(init_angles[angle_index])+'degrees.csv')
    return(angle_dict)

def get_cd_function(init_vels, init_alts, init_angle, apogee, vehicle_file, drag_data):
    data = np.zeros((len(init_vels), len(init_alts)))
    vadata = []
    cd_data = []
    for v_index in range(len(init_vels)):
        cur_vel = init_vels[v_index]
        for alt_index in range(len(init_alts)):
            cur_alt = init_alts[alt_index]
            data[v_index, alt_index] = alt_opt(vehicle_data=vehicle_file,
                                                            init_vel=cur_vel,
                                                            init_angle=init_angle,
                                                            init_alt=cur_alt,
                                                            goal_alt=apogee,
                                                            drag_file=drag_data)
            print(alt_index+len(init_alts)*v_index, end = "\r")
            if data[v_index, alt_index] > 0:
                vadata.append([init_vels[v_index],init_alts[alt_index]])
                cd_data.append(data[v_index, alt_index])
                print(data[v_index, alt_index])
    vadata = np.array(vadata)
    cd_data = np.array(cd_data)
    poly = PolynomialFeatures(degree=2, include_bias=False)
    va_poly = poly.fit_transform(vadata)
    model = LinearRegression()
    model.fit(va_poly, cd_data)
    print(model.coef_)
    print(model.intercept_)

    
