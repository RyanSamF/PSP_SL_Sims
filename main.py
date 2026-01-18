import rocketpy as rp
from matplotlib import *
#import datetime
#import numpy as np
#import pandas
#import yaml
#import math
#import matplotlib.pyplot as plt
#import csv
#from zoneinfo import ZoneInfo
#import SLUIRP
#import SLUIRP.data
#import SLUIRP.data.OpenCSV
import SLUIRP.data.OpenYAML
#import SLUIRP.in_dev
#import SLUIRP.in_dev.GetCD
#import SLUIRP.sims
import SLUIRP.sims.RocketPySim
import SLUIRP.plotting.external_plots
import SLUIRP.in_dev.airbrakes_system.midair_sims
import SLUIRP.data.OpenCSV
import SLUIRP.plotting.external_plots
from SLUIRP.in_dev.airbrakes_system.create_airbrakes_table import airbrakes_table, get_cd_function
from SLUIRP.in_dev.airbrakes_system.midair_sims import midair_sim
from SLUIRP.in_dev.airbrakes_system.CD_slope_estimation import CD_curve_estimate
from SLUIRP.in_dev.MonteCarlo.stochastic_sims import montecarlo_sim
from SLUIRP.plotting.sim_plots import drift_map
#import dill
#import time
import numpy as np
from SLUIRP.in_dev.airbrakes_system.Airbrakes import airbrakes_sim, airbrakes_multi
import pandas
from SLUIRP.plotting.sim_plots import param_graph
import matplotlib.pyplot as plt


def main():
    data = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/feustel_subscale_flight2.csv")
    vehicle = "ConfigFiles/feustel_cdr.yaml"
    angles = [5,5,7.5,7.5,10]
    speeds = [0,5,10,15,20]
    airbrakes_multi(vehicle = vehicle, 
                angles = angles,
                speeds = speeds, 
                lookup_csv = 'CSV_files/CFD_lookup.csv', 
                drag = 'CSV_files/air_brakes_drag.csv')
    '''
    angles = [5, 5, 7.5, 7.5, 10]
    speeds = [0, 5, 10, 15, 20]
    vehicle = "ConfigFiles/feustel_cdr.yaml"
    FT_TO_M = 3.28084
    df = pandas.read_csv('CSV_files/stuff.csv', index_col=None)
    time = np.array(df[df.columns[0]].tolist())
    alt = np.array(df[df.columns[1]].tolist())* FT_TO_M
    vel = np.array(df[df.columns[2]].tolist())* FT_TO_M
    accel = np.array(df[df.columns[3]].tolist()) * FT_TO_M
    param_graph(time, alt, vel, accel, 0, 0, "PID Controller",ejections=None)
    

    
    table = airbrakes_table(init_vels=range(10, 210, 5),
                    init_alts=range(75, 1335,10),
                    init_angles=[0 ],
                    apogee=1311,
                    vehicle_file="ConfigFiles/feustel_cdr.yaml",
                    drag_data="CSV_files/feustel_pdr_drag.csv")
    '''
    #drift_map([569.07,1151.33,1676.40,2258.67], speeds[1:], 2500, "OpenRocket", " | Constant Drift Speed, Apogee Above Launch")
    #SLUIRP.plotting.external_plots.graph_OR()
    #vfile = SLUIRP.data.OpenYAML.readYaml("ConfigFiles/feustel_subscale.yaml")
    #SLUIRP.sims.RocketPySim.single_sim(angle=6, speed=0, file_name=vehicle, name = None, markers = 1, iteration = None)
    #SLUIRP.sims.RocketPySim.multi_sim(angles = angles, speeds=speeds, vehicle=vehicle, markers = 1)
    #SLUIRP.plotting.external_plots.graph_OR()
    """
    montecarlo_sim(
            rocket_filepath=vehicle, 
                thrust_filepath='CSV_files/L1482_thrust.csv', 
                drag_filepath='CSV_files/feustel_pdr_drag_clone.csv', 
                thrust_MOE=0.025, 
                drag_MOE=0.05, 
                mass_MOE=0.05, 
                COG_MOE=0.05, 
                wind_dir_max=45, 
                wind_mean=8.7, 
                wind_std=3.5, 
                n=1000,
                airbrakes_drag = 'CSV_files/air_brakes_drag.csv', 
                lookup_csv = 'CSV_files/CFD_LU.csv')
    """
    '''
    SLUIRP.sims.RocketPySim.multi_sim(angles = angles, speeds=speeds, vehicle=vehicle, markers = 1)
    
    

    vehicle = SLUIRP.data.OpenYAML.readYaml("ConfigFiles/feustel_cdr.yaml")
    print(vehicle.area)
    print("working")
    data = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/OR_cdr.csv")
    env = SLUIRP.sims.RocketPySim.get_windy_env([2025, 11, 22, 12], 40.509294, -87.023958)
    env = SLUIRP.sims.RocketPySim.get_ST_env(5)
    
    
    environment = SLUIRP.sims.RocketPySim.get_ST_env(0*0.44704)
    #env = SLUIRP.sims.RocketPySim.get_windy_env([2025, 11, 22, 12], 40.509294, -87.023958)
    #env.plots.all()
    #SLUIRP.plotting.external_plots.compare_sim_real(vdf_data=data, env =environment, ws = 6, aoa = 0, flight_name = "Subscale Flight 2", vehicle =vfile)
    #mach_curve, cd_curve = CD_curve_estimate(drag_curve="CSV_files/feustel_pdr_drag.csv",cur_mach=0.262, cur_cd=0.75)
    #cur_apogee = midair_sim(vehicle_data="ConfigFiles/feustel_pdr.yaml",
    #                        init_vel=187,
    #                        init_alt= 1,
    #                        init_angle=0,
    #                        drag_data = np.column_stack([mach_curve, cd_curve]))
    #print(cur_apogee)
    #print(range(300, 4400,205))
   
    """
    table = airbrakes_table(init_vels=range(10, 210, 5),
                    init_alts=range(75, 1335,10),
                    init_angles=[0  ],
                    apogee=1341,
                    vehicle_file="ConfigFiles/feustel_cdr.yaml",
                    drag_data="CSV_files/feustel_pdr_drag.csv")
       
    get_cd_function(init_vels=range(100, 210, 5),
                    init_alts=range(75, 1335,10),
                    init_angle=0,
                    apogee=1341,
                    vehicle_file="ConfigFiles/feustel_cdr.yaml",
                    drag_data="CSV_files/feustel_pdr_drag.csv")
    """

    #env = SLUIRP.sims.RocketPySim.get_ST_env(8.7 * 0.3048)
    #vehicle = SLUIRP.data.OpenYAML.readYaml("ConfigFiles/feustel_pdr.yaml")
    #vdf = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/huntsvillelaunch.csv")
    #SLUIRP.plotting.external_plots.compare_sim_real(vdf, env, 6.5, "OpenRocket", vehicle)
    #vehicle = SLUIRP.data.OpenYAML.readYaml("ConfigFiles/feustel_pdr.yaml")
    #compare_sim_real(vdf_data, env, 3, "VDF Flight")
    #graph_thrust()
    #drag = np.array([[0, 0.8],[0.3, 0.9],[0.5,1]])
    #print(SLUIRP.in_dev.airbrakes_system.midair_sims.midair_sim("ConfigFiles/2026_Proposal_12lb.yaml", 50, 300, 50 , drag))
    #SLUIRP.sims.RocketPySim.multi_sim(angles, speeds, "ConfigFiles/feustel_cdr.yaml")
'''
if __name__ == "__main__":
    main()
    #[h_time,h_alt, h_vel, h_acc, h_temp, h_pres] = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/huntsville_data.csv")
    #h_dens = SLUIRP.in_dev.GetCD.get_density(h_temp, h_pres)
    #SLUIRP.in_dev.GetCD.CD_estimate(h_time,h_alt, h_vel, h_acc, h_dens, 0.01344,12.06556)