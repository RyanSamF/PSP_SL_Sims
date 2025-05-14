import pandas
import numpy as np
import csv

def get_standard_data(csv_file):
    #################################################################
    # gets time, altitude, velocity and acceleration from
    # OpenRocket created CSV file for use in plotting functions
    # INPUTS:
    # csv_file - filepath of csv file of open rocket data
    # OUTPUTS:
    # [time, alt, vel, accel] - vertical movement data
    #################################################################
    df1 = pandas.read_csv(csv_file, index_col=None)
    time = np.array(df1[df1.columns[0]].tolist())
    alt = np.array(df1[df1.columns[1]].tolist())
    vel = np.array(df1[df1.columns[2]].tolist())
    accel = np.array(df1[df1.columns[3]].tolist())
    return([time, alt, vel, accel])