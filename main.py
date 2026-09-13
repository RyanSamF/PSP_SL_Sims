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
    data = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/huntsville.csv")
    v_file= "ConfigFiles/feustel_vdf.yaml"
    veh = SLUIRP.data.OpenYAML.readYaml(v_file)
    veh.draw()
    drag = "CSV_files/VDF_airbrakes.csv"
    angles = [6,5,7.5,7.5,10]
    speeds = [10, 5,10,15,20]
    env = SLUIRP.sims.RocketPySim.get_ST_env(4.4704)
    #SLUIRP.sims.RocketPySim.multi_sim(angles, speeds, v_file)
    SLUIRP.plotting.external_plots.compare_sim_real(data, env, 10, 10, "Competition Flight", veh)
   
if __name__ == "__main__":
    main()
    #[h_time,h_alt, h_vel, h_acc, h_temp, h_pres] = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/huntsville_data.csv")
    #h_dens = SLUIRP.in_dev.GetCD.get_density(h_temp, h_pres)
    #SLUIRP.in_dev.GetCD.CD_estimate(h_time,h_alt, h_vel, h_acc, h_dens, 0.01344,12.06556)