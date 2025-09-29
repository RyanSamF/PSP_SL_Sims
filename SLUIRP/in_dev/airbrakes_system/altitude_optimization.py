"""
alt_optimize()
Get Cd value at starting mach number and starting altitude to reach desired altitude
    INPUT:
        Starting mach number
        Rocket data
        Starting altitude
        Starting angle
        Desired altitude

        Function 3 output
    OUTPUT: CD value to reach desired altitude

    1) run function 1 with input CD value (probably 0% deployment)
    2) Look at output of function 1 and adjust CD value input based on difference in height 
    3) Repeat 1 and 2 until output altitude = desired altitude (while loop)
"""