from cubesat_eps.battery import Battery
from cubesat_eps.solar_panel import SolarPanel
from cubesat_eps.power_manager import PowerManager
from utils import cubesatEPS


def main():
    # Initialize the models' objects
    battery = Battery(capacity_ah=6.4, voltage_v=8.2, soc_initial=0.8, charge_eff=0.95, discharge_eff=0.95, method="coulomb")
    solar_panel = SolarPanel(max_power_w=20, efficiency=0.2, area_m2=0.2)
    power_manager = PowerManager(voltage=8.2)
    
    satellite = cubesatEPS(battery, solar_panel, power_manager)

    # Simulation parameters
    sim_time_s = 86400
    time_step_s = 60
    
    # Execute simulation
    results = satellite.run_simulation(sim_time_s, time_step_s)
    
    # Plot results
    satellite.plot_results(results)

if __name__ == "__main__":
    main()
