import rocketpy
import random
from SLUIRP.data.OpenYAML import readYaml
import numpy as np
import pandas as pd
from SLUIRP.sims.RocketPySim import get_ST_env
import matplotlib.pyplot as plt
import joblib
from SLUIRP.in_dev.airbrakes_system.Airbrakes import controller
FT_TO_M = 3.28084

def montecarlo_sim(rocket_filepath, thrust_filepath, drag_filepath, thrust_MOE, drag_MOE, mass_MOE, COG_MOE, wind_dir_max, wind_mean, wind_std, n, airbrakes_drag = None, lookup_csv = None):
    ##################################################
    # Runs a series of simulations with random input variables
    # within a set margin of error.
    # INPUTS:
    # rocket_filepath - filepath of the rocket YAML file
    # thrust_filepath - filepath of the thrust csv file
    # drag_fileapth - filepath of the drag csv file
    # thrust_MOE - maximum error margin for thrust (multiplied 0.05 = 5%)
    # drag_MOE - maximum error margin for drag (multiplied 0.05 = 5%)
    # mass_MOE - maximum error margin for mass (multiplied 0.05 = 5%)
    # COG_MOE - maximum error margin for center of gravity (multiplied 0.05 = 5%)
    # wind_dir_max - maximum angle between wind direction and launch direction
    # wind_mean - mean wind speed for normal distribution
    # wind_std - standard deviation of wind speed for normal distribution
    # n - number of simulations
    # airbrakes_drag - filepath of drag csv file with airbrakes deployment level
    # lookup_csv - filepath of csv file showing deployment level based on altitude and velocity

    # OUTPUTS:
    # None - plots thrust.png to plots folder
    ##################################################

    # Set up arrays from csv files
    thrust_arrays = pd.read_csv(thrust_filepath, header=None)
    drag_arrays = pd.read_csv(drag_filepath)

    apogees = []
    if lookup_csv is None or airbrakes_drag is None:
        #No Air Brakes
        apogees = joblib.Parallel(n_jobs=-1)(joblib.delayed(single_stochastic)(rocket_filepath = rocket_filepath,
                                                                                thrust_arrays = thrust_arrays,
                                                                                drag_arrays = drag_arrays, 
                                                                                thrust_MOE = thrust_MOE, 
                                                                                drag_MOE = drag_MOE,
                                                                                mass_MOE = mass_MOE,
                                                                                COG_MOE = COG_MOE, 
                                                                                wind_dir_max = wind_dir_max, 
                                                                                wind_mean = wind_mean, 
                                                                                wind_std=wind_std,
                                                                                i = i) for i in range(n))
    else:
        # Air Brakes
        drag_arrays = pd.read_csv(airbrakes_drag)
        apogees = joblib.Parallel(n_jobs=-1)(joblib.delayed(single_stochastic_airbrakes)(rocket_filepath = rocket_filepath,
                                                                                thrust_arrays = thrust_arrays,
                                                                                drag_arrays = drag_arrays, 
                                                                                thrust_MOE = thrust_MOE, 
                                                                                drag_MOE = drag_MOE,
                                                                                mass_MOE = mass_MOE,
                                                                                COG_MOE = COG_MOE,  
                                                                                wind_dir_max = wind_dir_max, 
                                                                                wind_mean = wind_mean, 
                                                                                lookup_csv = lookup_csv,
                                                                                airbrakes_drag = airbrakes_drag,
                                                                                i = i) for i in range(n))
    counts, bins = np.histogram(a=apogees, bins = 25)
    plt.hist(bins[:-1], bins, weights=counts)
    if lookup_csv is None or airbrakes_drag is None:
        plt.title("Apogees from " + str(n) + " RocketPy Simulations")
    else:
        plt.title("Apogees from " + str(n) + " RocketPy Simulations with Air Brakes")
    plt.xlabel("Apogee (ft)")
    plt.ylabel("Frequency")
    plt.savefig("Plots/montecarlo.png")
    plt.show()
    print("Standard Deviation: "+str(np.std(apogees)))
    print("Mean: " +str(np.mean(apogees)))
    print("Median: " + str(np.median(apogees))) 
        
        
def single_stochastic(rocket_filepath, thrust_arrays, drag_arrays, thrust_MOE, drag_MOE, mass_MOE, COG_MOE, wind_dir_max, wind_mean, wind_std, i):
    cur_vehicle = readYaml(rocket_filepath)
    #Setting random inputs
    windspeed = np.random.normal(loc=wind_mean, scale=wind_std)
    windspeed = max(0, min(windspeed, 20))
    launch_inclination =90-np.interp(windspeed, [0, 5, 10, 15, 20], [5, 5, 6.5, 8, 10]) #Determines inclination from windspeed using linear interpolation
    launch_heading = 270 + random.randint(-100, 100)*wind_dir_max / 100
    thrust_change = random.randint(int(1000*(1-thrust_MOE)), int(1000*(1+thrust_MOE)))/1000
    drag_change = random.randint(int(1000*(1-drag_MOE)), int(1000*(1+drag_MOE)))/1000
    mass_change = random.randint(int(1000*(1-mass_MOE)), int(1000*(1+mass_MOE)))/1000
    COG_change = random.randint(int(1000*(1-mass_MOE)), int(1000*(1+COG_MOE)))/1000


    scaled_drag = drag_arrays
    scaled_drag['cD'] = scaled_drag['cD'] * drag_change
    scaled_drag_arrays = scaled_drag.to_numpy()
    scaled_thrust = thrust_arrays
    scaled_thrust[1] = scaled_thrust[1] * thrust_change
    scaled_thrust_arrays = scaled_thrust.to_numpy()

    cur_vehicle.motor.thrust_source = rocketpy.Function(scaled_thrust_arrays)
    cur_vehicle.power_off_drag = rocketpy.Function(scaled_drag_arrays)
    cur_vehicle.power_on_drag = rocketpy.Function(scaled_drag_arrays)
    cur_vehicle.total_mass = cur_vehicle.total_mass * mass_change
    cur_vehicle.center_of_dry_mass_position = cur_vehicle.center_of_dry_mass_position * COG_change
    env = get_ST_env(windspeed * 0.44704)
    flight = rocketpy.Flight(
            rocket = cur_vehicle, 
            environment = env, 
            rail_length = 3.6576, 
            inclination = launch_inclination, 
            heading = launch_heading,
            terminate_on_apogee=1)
    print(i, end='\r')
    return(flight.apogee * FT_TO_M)

def single_stochastic_airbrakes(rocket_filepath, lookup_csv, airbrakes_drag, thrust_arrays, drag_arrays, thrust_MOE, drag_MOE, mass_MOE, COG_MOE, wind_dir_max, wind_mean, i):
    cur_vehicle = readYaml(rocket_filepath)

    

    windspeed = np.random.normal(loc=wind_mean, scale=3.5)
    windspeed = max(0, min(windspeed, 20))
    launch_inclination =90-np.interp(windspeed, [0, 20], [5, 10]) #Determines inclination from windspeed using linear interpolation
    launch_heading = 270 + random.randint(-50, 50)*wind_dir_max / 100
    thrust_change = random.randint(int(1000*(1-thrust_MOE)), int(1000*(1+thrust_MOE)))/1000
    drag_change = random.randint(int(1000*(1-drag_MOE)), int(1000*(1+drag_MOE)))/1000
    drag_change = 1
    scaled_drag = drag_arrays
    scaled_drag['cd'] = scaled_drag['cd'] * drag_change
    scaled_drag_arrays = scaled_drag.to_numpy()
    scaled_thrust = thrust_arrays
    scaled_thrust[1] = scaled_thrust[1] * thrust_change
    scaled_thrust_arrays = scaled_thrust.to_numpy()

    cur_vehicle.motor.thrust_source = rocketpy.Function(scaled_thrust_arrays)
    cur_vehicle.power_off_drag = rocketpy.Function(scaled_drag_arrays)
    cur_vehicle.power_on_drag = rocketpy.Function(scaled_drag_arrays)
    env = get_ST_env(windspeed)
    air_brakes = cur_vehicle.add_air_brakes(
        drag_coefficient_curve=rocketpy.Function(scaled_drag_arrays),
        controller_function=controller,
        sampling_rate=10,   
        reference_area=None,
        clamp=True,
        initial_observed_variables=[0, 0, 0],
        override_rocket_drag=True,
        name=lookup_csv
    )
    flight = rocketpy.Flight(
            rocket = cur_vehicle, 
            environment = env, 
            rail_length = 3.6576, 
            inclination = launch_inclination, 
            heading = launch_heading,
            terminate_on_apogee=1,
            time_overshoot = False)
    print(i, end='\r')
    return(flight.apogee * FT_TO_M)




        


