from cubesat_eps.battery import Battery
from cubesat_eps.solar_panel import SolarPanel
from cubesat_eps.power_manager import PowerManager
from utils import cubesatEPS


def main():
    # Configuración de los módulos
    battery = Battery(capacity_ah=50, voltage_v=12, soc_initial=0.5, charge_eff=0.95, discharge_eff=0.95, method="coulomb")
    solar_panel = SolarPanel(max_power_w=10, efficiency=0.2, area_m2=0.1)
    power_manager = PowerManager(voltage=8.2)
    
    satellite = cubesatEPS(battery, solar_panel, power_manager)

    # Parámetros de simulación
    sim_time_s = 86400
    time_step_s = 60
    
    # Ejecutar simulación
    results = satellite.run_simulation(sim_time_s, time_step_s)
    
    # Mostrar resultados
    satellite.plot_results(results)

if __name__ == "__main__":
    main()
