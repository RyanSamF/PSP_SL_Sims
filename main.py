import rocketpy as rp
from matplotlib import *
import datetime
import numpy as np
import pandas
import yaml
import math
import matplotlib.pyplot as plt
import csv
from zoneinfo import ZoneInfo
import SLUIRP
import SLUIRP.data
import SLUIRP.data.OpenCSV
import SLUIRP.data.OpenYAML
import SLUIRP.sims
import SLUIRP.sims.RocketPySim
import SLUIRP.plotting
vdf_data = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/VDF_Flight.csv")



angles = [4, 5, 7.5, 7.5, 10]
speeds = [1, 5, 10, 15, 20]


wolf = SLUIRP.data.OpenYAML.readYaml("ConfigFiles/final_config.yaml")
#compare_sim_real(vdf_data, env, 3, "VDF Flight")
#graph_thrust()
SLUIRP.sims.RocketPySim.multi_sim(angles, speeds, wolf)
#graph_OR()
#testFlight.plots.trajectory_3d()
#testFlight.plots.all()
#testFlight.plots.aerodynamic_forces()
#testFlight.prints.all()
#print(wolf.center_of_mass())


#param_graph(time, alt, vel, accel, 7.4 , 3, "OpenRocket")