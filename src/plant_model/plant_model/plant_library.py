import numpy as np 
import scipy.optimize as opt
import matplotlib.pyplot as plt


def sigmoid(x, K, a, b):
    return K/(1 + np.exp(-a * (x - b)))


def sigmoid_fit(x_data, y_data):
    params, covariance = opt.curve_fit(sigmoid, x_data, y_data, p0=[max(y_data), 1, np.median(x_data)])
    # Extract the fitted parameters
    K_fit, a_fit, b_fit = params
    return K_fit, a_fit, b_fit


def pH_photosynthesis_CO2(k_pH, delta_pH): #  Returns CO2 absorption rate by the plant acconrding to the deviation of the pH of the soil. 
    delta_CO2 = -k_pH * delta_pH
    return delta_CO2


def Evaporation(R, moisture_history=[], sunlight_history = [], time_window = [0,10], dt=300):
    K_soil = 0 #  we can consider K_soil zero if we consider that the soil is well irrigated.
    L = (40.65*1000)/(18/1000) # Water Heat of vaporization in J/kg of water. 
    
    soil_mass = estimate_soil_mass(moisture_history, sunlight_history, time_window)
    water_mass_history = [ soil_mass*water_percentage/(1-water_percentage) for water_percentage in moisture_history]
    K_fit, A_fit, B_fit = sigmoid_fit(list(range(0,dt*len(water_mass_history),dt)) , water_mass_history)
    current_P_estimate = sigmoid(dt*len(water_mass_history), K_fit, A_fit, B_fit)
    Evaporation = current_P_estimate-K_soil/L + R/L #gives evaporation in kg/(s*m²)
    return Evaporation


def next_watering_estimate(percentage_threshold, R, moisture_history=[], sunlight_history = [], time_window = [0,10], dt=300):
    wm_init = estimate_water_mass(moisture_history, sunlight_history, time_window)
    sm = estimate_soil_mass(moisture_history, sunlight_history, time_window)
    evaporation = (R, moisture_history, sunlight_history, time_window, dt)
    t =  (wm_init*(1-percentage_threshold)-percentage_threshold*sm)/(evaporation*(1-percentage_threshold))
    return t 


def total_energy(sunlight_history=[], dt=300):
    total_E = 0 
    if len(sunlight_history)>0:
        for e in sunlight_history:
            total_E+=e*dt
    return total_E


def estimate_soil_mass(moisture_history=[], sunlight_history = [], time_window = [0,10]): # use night time window, one hour or less to neglect plant water usage
    if len(moisture_history=[])>(time_window[1]-time_window[0]) and len(sunlight_history)>(time_window[1]-time_window[0]):
        moisture_history = moisture_history[time_window[0]:time_window[1]]
        sunlight_history = sunlight_history[time_window[0]:time_window[1]]
    E = total_energy(sunlight_history, dt=300)
    L = 40.65/18
    Evaporated_water = L*E
    M1 = moisture_history[0]
    M2 = moisture_history[-1]
    soil_mass = Evaporated_water/(M1/(1-M1) + M2/(1-M2))
    return soil_mass


def estimate_water_mass(moisture_history=[], sunlight_history = [], time_window = [0,10]): # use night time window, one hour or less to neglect plant water usage
    soil_mass = estimate_soil_mass(moisture_history, sunlight_history, time_window)
    water_percentage = moisture_history[-1]
    water_mass = soil_mass*water_percentage/(1-water_percentage)
    return water_mass


def estimate_nutrient(nutrient_measurement, 
                      moisture_history=[], 
                      sunlight_history = [], 
                      nutrient_history=[], 
                      time_window=[0,10], dt = 86400): #generic function for NPK uptake estimate; also follows a sigmoid shape.
    
    soil_mass = estimate_soil_mass(moisture_history, sunlight_history, time_window)
    K_fit, a_fit, b_fit = sigmoid_fit(list(range(0,len(nutrient_history)*dt, dt))[time_window[0]:time_window[1]], 
                                      nutrient_measurement[time_window[0]:time_window[1]])
    nutrient_uptake_estimate = sigmoid(len(len(nutrient_history)), K_fit, a_fit, b_fit)
    return nutrient_uptake_estimate


def estimate_next_fertilization(nutrient_measurement, 
                                nutrient_threshold = 0,
                                moisture_history=[], 
                                sunlight_history = [], 
                                nutrient_history=[], 
                                time_window=[0,10], dt = 86400):
    
    soil_mass = estimate_soil_mass(moisture_history, sunlight_history, time_window)
    total_nutrient_mass = soil_mass * nutrient_measurement
    K_fit, a_fit, b_fit = sigmoid_fit(list(range(0,len(nutrient_history)*dt, dt))[time_window[0]:time_window[1]], 
                                      nutrient_measurement[time_window[0]:time_window[1]])
    nutrient_uptake_estimate = sigmoid(len(len(nutrient_history)), K_fit, a_fit, b_fit)
    return (total_nutrient_mass-nutrient_threshold)/nutrient_uptake_estimate


def plot_history(measurements, dt, time_window=[0,10], save=False, fig_name=""): #TODO: finish the plot function
    time = [i*dt/3600 for i in range(len(measurements))]
    measurements = measurements[time_window[0]:time_window[1]]
    # Set up plot with larger fonts
    plt.figure(figsize=(10, 6))
    # Plot the soil moisture data
    plt.plot(time, measurements, marker='o', linestyle='-', color='b')
    # Increase font size and labels
    plt.title('Soil Moisture Measurements Over 24 Hours', fontsize=18)
    plt.xlabel('Hour of the Day', fontsize=16)
    plt.ylabel('Soil Moisture (%)', fontsize=16)
    # Set x-ticks for every 3 hours and y-ticks with finer gridlines
    plt.xticks(np.arange(0, 24, step=3), fontsize=14)  # Only show x-ticks every 3 hours
    plt.yticks(fontsize=14)
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)  # Finer gridlines for y-axis
    # Remove borders and save as PDF
    plt.tight_layout(pad=0)  # Tight layout to remove borders
    plt.savefig("soil_moisture_measurements_compact_xaxis.pdf", bbox_inches='tight', format='pdf')
    # Show plot
    plt.show()