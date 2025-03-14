# function to generate 100 logistic growth curves

"""
this function generates multiple logistic growth curves with variations in lag phase and exponential phase.

A logistic growth curve represents population growth with a limit.
At first, the population grows slowly (lag phase), then grows rapidly (exponential phase),
before plateauing when it reaches its maximum limit (carrying capacity).


the equation:
P(t) = K / (1 + (K – P0) / P0 * e^(-rt)),
where,
    P(t) is the population at time t,
    K is the carrying capacity (maximum population limit),
    P0 is the initial population size,
    r is the intrinsic growth rate, and
    e is 2.71828 (Euler's number)


parameters for the logistic growth curve function include:
    num_curves (int): Number of growth curves to generate,
    K (int): Carrying capacity,
    P0 (int): Initial population size,
    max_time (int): Total simulation time,

"""
def generate_logistic_growth_curves(num_curves=100, K=1000, P0=10, E=2.71828, max_time=100):

    growth_curves = [] # create an empty list to store all the generated logistic growth curves

    for curve_index in range(num_curves): # for loop to generate multiple logistic growth curves
        lag_variation = (curve_index % 16) + 5  # variation from 5 to 20
        growth_rate = 0.12 + ((curve_index % 14) + 2) / 100
        curve_data = {"Time": [], "Population": [], "Curve": curve_index + 1}

        print(f"\nCurve {curve_index + 1}:")

        for time_step in range(max_time): # loop through time steps
            if time_step < lag_variation:  # lag phase where growth is minimal
                population_size = P0
            else:
                population_size = (K / (1 + ((K - P0) / P0) * (E ** (-growth_rate * (time_step - lag_variation)))))

            curve_data["Time"].append(time_step)
            curve_data["Population"].append(population_size)
            print(f"Time: {time_step}, Population: {population_size:.2f}")

        growth_curves.append(curve_data)

    return growth_curves

growth_curves = generate_logistic_growth_curves(num_curves=10, max_time=20) # generates the logistic growth curves
