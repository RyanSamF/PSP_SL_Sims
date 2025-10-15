import rocketpy as rp
import math 
import SLUIRP.data.OpenYAML
import time

def midair_sim(vehicle_data, init_vel, init_alt, init_angle, drag_data = None):
    ##################################################
    # Simulates midair launch given velocity and altitude
    # and returns apogee
    # INPUTS:
    # vehicle - name of csv file of vehicle being simulated
    # init_vel - initial velocity of vehicle (m/s)
    # init_alt - initial height of vehicle (m)
    # init_angle - initial angle from vertical of vehicle (degrees)
    # drag_data - (optional) 
    # OUTPUTS:
    # apogee - apogee in meters
    ##################################################
    #t1 = time.perf_counter()
    vehicle = SLUIRP.data.OpenYAML.readYaml(vehicle_data)
    #t2 = time.perf_counter() - t1
    if drag_data is not None:
        vehicle.power_off_drag = rp.Function(drag_data)
        vehicle.power_on_drag = rp.Function(drag_data)
    #t3 = time.perf_counter() - t1 - t2
    #sets up environment
    env = rp.Environment(latitude = 40.505404, longitude = -87.019832, elevation=187)
    env.set_date((2026, 4, 13, 6))
    #Creates environment using standard atmosphere and zero wind speed
    env.set_atmospheric_model(
        type="custom_atmosphere",
        wind_u = [(0,0)], #wind in one direction (m/s)
        wind_v = [(0,0)], #wind in perpendicular directon (m/s)
        pressure=None, #no change from standard atmosphere in pressure
        temperature=None) #no change from standard atmosphere in temperature
    #t4 = time.perf_counter() - t1 - t3
    init_angle = math.radians(init_angle)
    [q_0, q_1, q_2, q_3] = rp.tools.euler313_to_quaternions(init_angle, 0, 0) #converts pitch into quaternion
    vehicle.motor.propellant_mass = 0
    vehicle.motor.thrust_source = "CSV_files/zero.csv" #this is literally just a csv file with two zeros in it
    testFlight   = rp.Flight(
            rocket = vehicle,
            environment = env, 
            rail_length = 5, 
            inclination = 90, 
            heading = 270,
            initial_solution=[0, 0, 0, init_alt+env.elevation, 
                math.sin(init_angle) * init_vel, 0 , math.cos(init_angle) * init_vel,
                q_0, q_1, q_2, q_3, 0, 0, 0],
            terminate_on_apogee=1,
            atol = 6*1e-3 + 4*1e-6 + 3*1e-3,
            ode_solver = 'RK45' )
    #t5 = time.perf_counter() - t1 - t4
    #print("vehicle definition: ", t2)
    #print("drag definition:", t3)
    #print("enviornment definition", t4)
    #print("flight simulation:", t5)
    #testFlight.plots.trajectory_3d()
    return(testFlight.apogee)
    


"""midair_sim()
Simulate midair launch with starting velocity and altitude
    -INPUTS: rp.rocket class (vehicle data)
            Starting velocity/mach
            starting altitude
            Starting angle
    -OUTPUT:
        Apogee
"""