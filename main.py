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
import SLUIRP.in_dev
import SLUIRP.in_dev.GetCD
import SLUIRP.sims
import SLUIRP.sims.RocketPySim
import SLUIRP.plotting
import SLUIRP.in_dev.airbrakes_system.midair_sims
import dill
import time

def main():
    angles = [5, 5, 7.5, 7.5, 10]
    speeds = [0, 5, 10, 15, 20]

    #vehicle = SLUIRP.data.OpenYAML.readYaml("ConfigFiles/2026_Proposal_12lb.yaml")
    #compare_sim_real(vdf_data, env, 3, "VDF Flight")
    #graph_thrust()
    #drag = np.array([[0, 0.8],[0.3, 0.9],[0.5,1]])
    #print(SLUIRP.in_dev.airbrakes_system.midair_sims.midair_sim("ConfigFiles/2026_Proposal_12lb.yaml", 50, 300, 50 , drag))
    #SLUIRP.sims.RocketPySim.multi_sim(angles, speeds, "ConfigFiles/2026_Proposal_12lb.yaml", "for 12 lb Design")
    SLUIRP.sims.RocketPySim.single_sim(5, 0, "ConfigFiles/2026_Proposal_12lb.yaml", "for 12 lb Design")
    #graph_OR()
    #testFlight.plots.trajectory_3d()
    #testFlight.plots.aerodynamic_forces()
    #testFlight.prints.all()
    #print(wolf.center_of_mass())


    #param_graph(time, alt, vel, accel, 7.4 , 3, "OpenRocket")

if __name__ == "__main__":
    main()
    #[h_time,h_alt, h_vel, h_acc, h_temp, h_pres] = SLUIRP.data.OpenCSV.get_standard_data("CSV_files/huntsville_data.csv")
    #h_dens = SLUIRP.in_dev.GetCD.get_density(h_temp, h_pres)
    #SLUIRP.in_dev.GetCD.CD_estimate(h_time,h_alt, h_vel, h_acc, h_dens, 0.01344,12.06556)