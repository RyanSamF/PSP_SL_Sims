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
#import dill
#import time
import numpy as np
from SLUIRP.in_dev.airbrakes_system.Airbrakes import airbrakes_sim, airbrakes_multi
def main():
    angles = [5, 5, 7.5, 7.5, 10]
    speeds = [0, 5, 10, 15, 20]
    vehicle = "ConfigFiles/feustel_cdr.yaml"
    airbrakes_multi(vehicle = vehicle, 
                angles = angles,
                speeds = speeds, 
                lookup_csv = 'CSV_files/CFD_lookup.csv', 
                drag = 'CSV_files/air_brakes_drag.csv')
    """
    vehicle = SLUIRP.data.OpenYAML.readYaml("ConfigFiles/feustel_cdr.yaml")
    print(vehicle.area)
    print("working")
    data = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/OR_cdr.csv")
    #env = SLUIRP.sims.RocketPySim.get_windy_env([2025, 11, 22, 12], 40.509294, -87.023958)
    env = SLUIRP.sims.RocketPySim.get_ST_env(5)
    SLUIRP.plotting.external_plots.compare_sim_real(data, env, 0, "Subscale", vehicle)
    """
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

if __name__ == "__main__":
    main()
    #[h_time,h_alt, h_vel, h_acc, h_temp, h_pres] = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/huntsville_data.csv")
    #h_dens = SLUIRP.in_dev.GetCD.get_density(h_temp, h_pres)
    #SLUIRP.in_dev.GetCD.CD_estimate(h_time,h_alt, h_vel, h_acc, h_dens, 0.01344,12.06556)