import numpy as np
import matplotlib.pyplot as plt
from cubesat_eps.battery import Battery
from cubesat_eps.solar_panel import SolarPanel
from cubesat_eps.power_manager import PowerManager

class cubesatEPS:

    def __init__(self, battery: Battery, solar_panel: SolarPanel, power_manager: PowerManager):
        self.battery = battery
        self.solar_panel = solar_panel
        self.power_manager = power_manager

    def run_simulation(self, sim_time_s, time_step_s):
        """
        Runs the CubeSat EPS simulation.
        """
        time = np.arange(0, sim_time_s + time_step_s, time_step_s)
        soc = np.zeros_like(time, dtype=float)
        soc[0] = self.battery.soc

        subsystem_states = {name: [] for name in self.power_manager.subsystems_consumption.keys()}


        for subs in self.power_manager.subsystems_consumption.keys():
                subsystem_states[subs].append(False)

        power_generated = np.array([self.solar_panel.get_power_output(t) for t in time])
        current_generated = power_generated / self.battery.voltage_v
        power_total_load = sum(self.power_manager.subsystems_consumption.values())
        current_load = power_total_load / self.battery.voltage_v
        
                
        for i in range(1, len(time)):
            I_net = current_generated[i] - current_load
            I_net = I_net * self.battery.charge_eff if I_net > 0 else I_net / self.battery.discharge_eff
            soc[i] = soc[i-1] + (I_net * time_step_s) / (self.battery.capacity_ah * 3600)
            soc[i] = np.clip(soc[i], 0.0, 1.0)
            states = self.power_manager.manage_energy(I_net)
            for subs in self.power_manager.subsystems_consumption.keys():
                subsystem_states[subs].append(states[subs])
        
        for subs in self.power_manager.subsystems_consumption.keys():
            subsystem_states[subs] = np.array(subsystem_states[subs])
        
        return time, power_generated, soc, current_generated, current_load, subsystem_states

    def plot_results(self, results):
        """
        Plots the simulation results.
        """
        time, power_generated, soc, current_generated, current_load, subsystem_states = results
        time_hours = time / 3600
        
        plt.figure(figsize=(14, 10))
        
        plt.subplot(4, 1, 1)
        plt.plot(time_hours, power_generated, label='Generated Power (W)', color='orange')
        plt.axhline(y=current_load * self.battery.voltage_v, color='blue', linestyle='--', label='Total Power Consumption (W)')
        plt.title('Power Generation and Consumption')
        plt.xlabel('Time (hours)')
        plt.ylabel('Power (W)')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(4, 1, 2)
        plt.plot(time_hours, soc * 100, label='State of Charge (SOC)', color='purple')
        plt.title('Battery SOC')
        plt.xlabel('Time (hours)')
        plt.ylabel('SOC (%)')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(4, 1, 3)
        for subs, state in subsystem_states.items():
            plt.plot(time_hours, state, label=subs)
        plt.title('Subsystems Status')
        plt.xlabel('Time (hours)')
        plt.ylabel('Status (1=On, 0=Off)')
        plt.legend()
        plt.grid(True)
        
        plt.subplot(4, 1, 4)
        plt.plot(time_hours, current_generated, label='Generated Current (A)', color='green')
        plt.axhline(y=current_load, color='red', linestyle='--', label='Consumed Current (A)')
        plt.title('Current Generation and Consumption')
        plt.xlabel('Time (hours)')
        plt.ylabel('Current (A)')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
