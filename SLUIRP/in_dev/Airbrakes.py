import rocketpy

def controller():
    print("Controller has not been implemented yet")


air_brakes = vehicle.add_air_brakes(
    drag_coefficient_curve="../data/rockets/calisto/air_brakes_cd.csv",
    controller_function=controller,
    sampling_rate=10,
    reference_area=None,
    clamp=True,
    initial_observed_variables=[0, 0, 0],
    override_rocket_drag=False,
    name="Air Brakes",
)
