import matplotlib.pyplot as plt
import numpy as np
import scipy
import SLUIRP.plotting.external_plots
import SLUIRP.plotting.sim_plots
import pandas

def CD_estimate(time,alt, vel, accel, density, area, mass):
    df1 = pandas.read_csv("CSV_files/TestHuntsville.csv", index_col=None)
    testtime = np.array(df1[df1.columns[0]].tolist())
    testalt = np.array(df1[df1.columns[1]].tolist())*0.3048
    time = time - time[0]
    #for t in range(1,len(time)-1):
    #    if time[t] - time[t-1] < 0.01:
    #        time[t] = time[t-1] + 0.001
    testalt = smooth(testalt, 100)
    print(len(alt))
    print(len(time))
    vel1 = np.gradient(testalt, testtime)
    accel1 = np.gradient(vel1, testtime)
    vel1 = smooth(vel1, 100)
    accel1 = smooth(accel1, 100)
    print(len(vel1))
    print(len(accel1))
    est_CD = (2* (abs(accel + 9.807) ) * mass)/ (density * area * (vel) ** 2)
    plot2 = plt.plot(time, est_CD)
    plt.show()
    SLUIRP.plotting.external_plots.compare_graph([time, alt, vel, accel],
                                                 [testtime, testalt, vel1, accel1],
                                                 10,
                                                 5,
                                                 "real",
                                                 "integrated")
    

    
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def get_density(temp, pressure):
    return((pressure / 1000) / (0.2869 * (temp + 273.15)))

