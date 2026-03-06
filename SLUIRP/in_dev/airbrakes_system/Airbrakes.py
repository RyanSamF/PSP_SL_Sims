import rocketpy as rp
import pandas as pd
from scipy.interpolate import interpn, RegularGridInterpolator
from SLUIRP.sims.RocketPySim import get_ST_env
from SLUIRP.plotting.sim_plots import prof_graph, param_graph
from SLUIRP.data.OpenYAML import readYaml
import joblib
import csv
import matplotlib.pyplot as plt
import numpy as np

FT_TO_M = 3.28084
IN_TO_M = 1 / 39.37
LBS_TO_KG = 0.4536



def VDF_controller(time, sampling_rate, state, state_history, observed_variables, air_brakes):
    if observed_variables[-1][0] == time:
        return(None)
    if time < 5.32:
        return (time, 0)
    else:
        new_deployment_level = 1
    max_change = 0.59 / sampling_rate
    lower_bound = air_brakes.deployment_level - max_change
    upper_bound = air_brakes.deployment_level + max_change
    new_deployment_level = min(max(new_deployment_level, lower_bound), upper_bound)
    air_brakes.deployment_level = new_deployment_level
    return (
        time,
        air_brakes.deployment_level
    )

def standard_controller(time, sampling_rate, state, state_history, observed_variables, air_brakes):
    # state = [x, y, z, vx, vy, vz, e0, e1, e2, e3, wx, wy, wz]
    lookup_table = pd.read_csv(air_brakes.name, index_col=0)
    interp_table = RegularGridInterpolator(
        (lookup_table.index, lookup_table.columns), lookup_table.values, method='linear'
    )
    alt = state[2]
    vel = state[5]  
    if alt < 75:
        new_deployment_level = 0
    #CHANGE HARD CODED VALUE TO MAX ALT IN LOOKUP TABLE
    elif alt > 1325:
        new_deployment_level = 1
    elif vel > 10 and vel < 205:
        new_deployment_level = interpn([lookup_table.index, lookup_table.columns], lookup_table.values, (vel, alt), method='linear')
    else:
        new_deployment_level = 0
    max_change = 6 / sampling_rate
    lower_bound = air_brakes.deployment_level - max_change
    upper_bound = air_brakes.deployment_level + max_change
    new_deployment_level = min(max(new_deployment_level, lower_bound), upper_bound)
    air_brakes.deployment_level = new_deployment_level
    return (
        time,
        air_brakes.deployment_level
    )


def airbrakes_sim(vehicle_file, angle, windspeed, lookup_csv, drag, name = "Air Brakes", iteration = None, control = None):
    vehicle = readYaml(vehicle_file)
    end_results = None
    if control in function_map:
        controller = function_map[control]
    else:
        controller = standard_controller
    env = get_ST_env(windspeed * 0.44704)
    air_brakes = vehicle.add_air_brakes(
        drag_coefficient_curve=drag,
        controller_function=controller,
        sampling_rate=10,   
        reference_area=None,
        clamp=True,
        initial_observed_variables=[0, 0, 0],
        override_rocket_drag=True,
        name=lookup_csv
    )
    airbrakes_flight= rp.Flight(
        rocket=vehicle,
        environment=env,
        rail_length=3.6576,
        inclination= 90 - angle,
        heading=270,
        time_overshoot=False,
        )
    time = airbrakes_flight.time
    vel_main_deploy = 0
    alt = airbrakes_flight.altitude(time) * FT_TO_M
    accel = airbrakes_flight.az(time) * FT_TO_M
    vel = airbrakes_flight.vz(time) * FT_TO_M
    mach_num = airbrakes_flight.mach_number(time)
    drift = -1 * airbrakes_flight.x(time) * FT_TO_M

    for vIndex in range(0,len(vel)):
    #Determines velocity and time of main deployment
        if vel_main_deploy == 0 and alt[vIndex] <= vehicle.main_deploy * 3.281 + 10 and vel[vIndex] < -1:
            vel_main_deploy = vel[vIndex]
            time_main_deploy = time[vIndex]
            #print("alt:" + str(alt[-1]))
    plot_name = param_graph(time, alt, vel, accel, windspeed, angle, "RocketPy Airbrakes", name)
    
    #Makes profile graphs for flight, altitude vs drift distance
    prof_graph(drift, alt, windspeed, angle, "RocketPy Airbrakes", name)

    #Plots Deployment level vs time
    time_list, deployment_level_list = [], []
    obs_vars = airbrakes_flight.get_controller_observed_variables()
    for array in obs_vars:
        time_d = array[0]
        deployment_level = array[1]
        if type(deployment_level) != int and type(deployment_level) != float:
            deployment_level = deployment_level[0]
        time_list.append(time_d)
        deployment_level_list.append(deployment_level)
    # Plot deployment level by time
    fig, ax1 = plt.subplots()
    ax1.set_ylabel("Deployment")
    ax1.set_xlabel('Time (s)')
    ax1.set_ylim(0,1)
    ax1.set_xlim(0,airbrakes_flight.apogee_time)
    lns3 = ax1.plot(time_list, deployment_level_list, color=(1, 0, 0))
    plt.title("Deployment Level by Time "+str(windspeed) + " mph " + str(angle) + " Degrees")
    plt.grid()
    plt.savefig('Plots/' + "deployment"+ str(windspeed) +"_" + str(angle) + ".png", format='png')


    final_vel= vel[-1]
    stability= airbrakes_flight.stability_margin(airbrakes_flight.out_of_rail_time + 5)
    descent_time= time[-1] - airbrakes_flight.apogee_time
    ascent_time= airbrakes_flight.apogee_time
    apogee= (airbrakes_flight.apogee - env.elevation) * FT_TO_M
    print(apogee)
    distance= abs(drift[-1])
    run_params= plot_name
    max_mach= max(mach_num)
    max_vel= max(vel)
    max_accel= max(accel)
    max_ke= 0.5 * vel[-1] ** 2 * vehicle.m_heav / 32.17
    vel_at_main= vel_main_deploy
    under_drogue= time_main_deploy - airbrakes_flight.apogee_time
    #print("after" + str(time_main_deploy))
    under_main=(time[-1] - time_main_deploy)

    end_results = [run_params, 
            final_vel,
            descent_time,
            ascent_time,
            apogee, 
            distance, 
            max_vel, 
            max_accel, 
            max_mach, 
            max_ke, 
            under_drogue, 
            under_main,
            vel_at_main]
    return(end_results)


def airbrakes_multi(vehicle, angles, speeds, lookup_csv, drag):
    speeds_ms = [x * 0.44704 for x in speeds]
    env_arr = [None] * len(speeds)
    #time =  datetime.datetime(2025, 2, 23, 13, 30, 0, 0, tzinfo=ZoneInfo("America/Indianapolis"))
    for i in range(len(speeds_ms)):
        env = get_ST_env(speeds_ms[i])
        env_arr[i] = (env)

    #Data labels for final output csv file, all final data is appended to these lists
    final_vel = "Final Velocity (ft/s)"
    stability = "Stability off rod (calibers)"
    descent_time = "Descent Time (seconds)" 
    ascent_time = "Ascent Time (seconds)"
    apogee = "Apogee (ft)"
    distance = "Drift Distance (ft)"
    max_mach = "Max Mach Number"
    max_vel = "Max Velocity (ft/s)" 
    max_accel = "Max Acceleration (ft/s)"
    max_ke = "Max Kinetic Energy (ft-lbf)"
    under_drogue = "Time Under Drogue (sec)" 
    under_main = "Time Under Main (sec)"
    vel_at_main = "Velocity at Main Deployment (ft/s)" 
    run_params = ""
    end_results = [None]*(len(angles) + 1)
    labels = [run_params, 
            final_vel,
            descent_time,
            ascent_time,
            apogee, 
            distance, 
            max_vel, 
            max_accel, 
            max_mach, 
            max_ke, 
            under_drogue, 
            under_main,
            vel_at_main]
    #simulates launch and records above data for each pair of wind speeds and angles 
    end_results = joblib.Parallel(n_jobs=-1)(joblib.delayed(airbrakes_sim)(angle=angles[i],
                                                                            windspeed = speeds[i], 
                                                                            vehicle_file =vehicle, 
                                                                            lookup_csv = lookup_csv,
                                                                            drag = drag,
                                                                            iteration = i) for i in range(len(speeds)))
    end_results.insert(0, labels)
    end_results = [list(row) for row in zip(*end_results)]
    """PROBABLY WANT TO MAKE THIS IT'S OWN FUNCTION AT SOME POINT"""
    # Specify the file name
    filename = "output.csv"
    # Open the file in write mode
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        # Write each row to the CSV file
        writer.writerows(end_results)

    print(f"Data written to {filename}")

function_map = {'VDF':VDF_controller,
                'standard':standard_controller}