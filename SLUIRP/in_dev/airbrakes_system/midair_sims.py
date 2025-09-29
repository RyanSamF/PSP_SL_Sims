import rocketpy as rp
import math 

def midair_sim(vehicle, init_vel, init_alt, init_angle):
    ##################################################
    # Simulates midair launch given velocity and altitude
    # and returns apogee
    # INPUTS:
    # vehicle - vehicle being simulated
    # init_vel - initial velocity of vehicle (m/s)
    # init_alt - initial height of vehicle (m)
    # init_angle - initial angle from vertical of vehicle (degrees)
    # OUTPUTS:
    # apogee - apogee in meters
    ##################################################
    
    env = rp.Environment(latitude = 40.505404, longitude = -87.019832, elevation=187)
        #URL = "http://weather.uwyo.edu/cgi-bin/sound   ing?region=naconf&TYPE=TEXT%3ALIST&YEAR=2024&MONTH=04&FROM=1300&TO=1312&STNM=72230"
    env.set_date((2024, 4, 13, 6))
    #Creates environment using standard atmosphere, and defining wind at 0 and 5000 meters as wind speed
    env.set_atmospheric_model(
        type="custom_atmosphere",
        wind_u = [(0,0)], #wind in one direction (m/s)
        wind_v = [(0,0)], #wind in perpendicular directon (m/s)
        pressure=None, #no change from standard atmosphere in pressure
        temperature=None) #no change from standard atmosphere in temperature
    init_angle = math.radians(init_angle)
    [q_0, q_1, q_2, q_3] = rp.tools.euler313_to_quaternions(init_angle, 0, 0)
    vehicle.motor.propellant_mass = 0
    vehicle.motor.thrust_source = "CSV_files/zero.csv"
    testFlight   = rp.Flight(
            rocket = vehicle,
            environment = env, 
            rail_length = 5, 
            inclination = 90, 
            heading = 270,
            initial_solution=[0, 0, 0, init_alt+env.elevation, 
                math.sin(init_angle) * init_vel, 0 , math.cos(init_angle) * init_vel,
                q_0, q_1, q_2, q_3, 0, 0, 0],
            terminate_on_apogee=1)
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