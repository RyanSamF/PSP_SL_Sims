import rocketpy
import random
from SLUIRP.data.OpenYAML import readYaml
import numpy as np

def montecarlo_sim(rocket_filepath, thrust_MOE, drag_MOE, wind_dir_max, wind_mean n):
    base_vehicle = readYaml(rocket_filepath)
    for run_num in range(n):
        windspeed = np.random.normal(loc=wind_mean, scale=3.5)
        windspeed = max(0, min(windspeed, 20))
        launch_inclination =90-np.interp(windspeed, [0, 20], [5, 10]) #Determines inclination from windspeed using linear interpolation
        heading = 270 + random.randint(-50, 50)*wind_dir_max / 100

        thrust_change = random.randint(1000*(1-thrust_MOE), 1000*(1+thrust_MOE))/1000
        drag_change = random.randint(1000*(1-drag_MOE), 1000*(1+drag_MOE))/1000

