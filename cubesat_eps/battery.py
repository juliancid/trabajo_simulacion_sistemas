import numpy as np

class Battery:
    """
    Models a battery system for a CubeSat EPS.

    Methods:
    --------
        update_soc(current_a, dt_s, voltage=None)
            Updates the SOC using the selected estimation method.

        energy_available()
            Returns the available energy in Wh.

        capacity_remaining()
            Returns the remaining capacity in Ah.

        simulate_degradation()
            TBD: Simulate battery capacity degradation over time.

        simulate_temperature_effect()
            TBD: Adjust efficiency based on battery temperature.
    """
     
    def __init__(self, capacity_ah: float, voltage_v: float, soc_initial=0.5, charge_eff=0.95, discharge_eff=0.95, method="coulomb"):
        """
        Args:
            capacity_ah (float): Capacity of the battery pack in Ah.
            voltage_v (float): Voltage of the battery pack in V.
            soc_initial (float, optional): Initial value of the SoC to start the simulation. Defaults to 0.5.
            charge_eff (float, optional): Charge efficiency. Defaults to 0.95.
            discharge_eff (float, optional): Discharge efficiency Defaults to 0.95.
            method (str, optional): Model to update SoC {coulomb, kalman, h_infinity}. Defaults to "coulomb".
        """

        self.capacity_ah = capacity_ah
        self.voltage_v = voltage_v
        self.soc = soc_initial
        self.charge_eff = charge_eff
        self.discharge_eff = discharge_eff
        self.method = method

    def update_soc(self, current_a, dt_s, voltage=None):
        """Update the SoC based on the selected estimation method."""
        if self.method == "coulomb":
            self._update_coulomb(current_a, dt_s)
        elif self.method == "kalman" and voltage is not None:
            self._update_kalman(current_a, voltage)
        elif self.method == "h_infinity" and voltage is not None:
            self._update_h_infinity(current_a, voltage)
        else:
            print("Method selected not valid!")

        # Ensure SOC remains in the valid range
        self.soc = np.clip(self.soc, 0, 1)

    def _update_coulomb(self, current_a, dt_s):
        """Coulomb counting method."""
        if current_a > 0:
            current_a *= self.charge_eff
        else:
            current_a /= self.discharge_eff
        self.soc += (current_a * dt_s) / (self.capacity_ah * 3600)

    def _update_kalman(self, current_a, voltage):
        """Placeholder for Kalman filter implementation."""
        print("To be developed.")

    def _update_h_infinity(self, current_a, voltage):
        """Placeholder for H-infinity filter implementation."""
        print("To be developed.")

    def energy_available(self):
        """
        Returns the available energy in Wh.

        Returns:
        --------
        float : Available energy in watt-hours (Wh).
        """
        return self.soc * self.capacity_ah * self.voltage_v

    def capacity_remaining(self):
        """
        Returns the remaining capacity in Ah.

        Returns:
        --------
        float : Remaining capacity in ampere-hours (Ah).
        """
        return self.soc * self.capacity_ah
    
    def simulate_degradation(self):
        """
        TBD: Simulates battery capacity degradation over time.

        Future Implementation:
        ----------------------
        - Model degradation as a function of cycles, depth of discharge, and temperature.
        - Adjust capacity_ah dynamically to reflect real-life aging effects.
        """
        pass  # Future implementation

    def simulate_temperature_effect(self):
        """
        TBD: Adjusts efficiency based on battery temperature.

        Future Implementation:
        ----------------------
        - Introduce a thermal model affecting charge/discharge efficiency.
        - Implement a temperature-dependent resistance model.
        """
        pass  # Future implementation