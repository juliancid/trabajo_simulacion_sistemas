import numpy as np

class PowerManager:
    """
    Class to manage power distribution among CubeSat subsystems.
    """
    def __init__(self, voltage=12):
        """
        Initializes the power manager.

        :param voltage: Nominal bus voltage of the EPS (V).
        """
        self.voltage = voltage
        self.subsystems_consumption = {
            'Communications': 7,    # Watts
            'Cameras': 5,           # Watts
            'Thermal Control': 2,   # Watts
            'Sensors': 1            # Watts
        }
        self.priority = {
            'Communications': 1,
            'Cameras': 2,
            'Thermal Control': 3,
            'Sensors': 4
        }

    def manage_energy(self, available_current):
        """
        Distributes available power among subsystems based on priority.

        :param available_current: Net available current (A).
        :return: Dictionary with the state of each subsystem (True=On, False=Off).
        
        TBD:
        - Implement a more dynamic priority system (e.g., based on mission phases).
        - Introduce a feedback mechanism to adjust priorities dynamically.
        """

        # Sort subsystems by priority and calculate total available power
        sorted_subsystems = sorted(self.subsystems_consumption.keys(), key=lambda x: self.priority[x])
        state = {name: False for name in self.subsystems_consumption.keys()}
        available_power = available_current * self.voltage

        # Loop through the subsystems, if the power necesary to turn on a subsystem is available, it turns on
        for subs in sorted_subsystems:
            power_required = self.subsystems_consumption[subs]
            if available_power >= power_required:
                state[subs] = True
                available_power -= power_required
            else:
                state[subs] = False  # Subsystem remains off

        return state
