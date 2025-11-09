import pandas
import numpy as np
import matplotlib.pyplot as plt
"""
CD_curve_estimate()
Estimate equation of Cd curve vs mach
    INPUT: 
    Mach vs CD csv file
    Mach number
    CD value

    OUTPUT: 
    Mach number vs CD csv file with linearized data from starting data points
    """



def CD_curve_estimate(drag_curve, cur_mach, cur_cd):
    df1 = pandas.read_csv(drag_curve, index_col=None)
    mach = np.array(df1[df1.columns[0]].tolist())
    cd = np.array(df1[df1.columns[1]].tolist())
    mask_low = mach < 0.04
    mask_high = mach > 0.04
    low_mach = mach[mask_low]
    low_cd = cd[mask_low]
    high_mach = mach[mask_high]
    high_cd = cd[mask_high]
    low_coef = np.polyfit(low_mach, low_cd, 2)
    high_coef = np.polyfit(high_mach, high_cd, 2)
    reg_mach = np.arange(0, max(mach), 0.001)
    reg_cd = np.zeros(len(reg_mach))
    for i in range(len(reg_mach)):
        if reg_mach[i] < 0.04:
            reg_cd[i] = reg_mach[i] ** 2 * low_coef[0] + reg_mach[i] * low_coef[1] + low_coef[2]
        else:
            reg_cd[i] = reg_mach[i] ** 2 * high_coef[0] + reg_mach[i] * high_coef[1] + high_coef[2]
    closest_index = np.argmin(np.abs(reg_mach - cur_mach))
    cd_diff = cur_cd - reg_cd[closest_index]
    final_cd = reg_cd + cd_diff
    final_cd[final_cd < 0] = 0
    return(reg_mach, final_cd)
    
