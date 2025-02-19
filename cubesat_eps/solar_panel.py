import numpy as np

class SolarPanel:
    """
    Models the power generation of the solar panels

    Methods:
    --------
        get_power_output(time_s)
            Calculates the power output with the incidence and irradiance
    """

    orbit_period = 5400     # LEO Orbit period in seconds (~90 min)
    solar_constant = 1361   # Amount of energy received by a given area one astronomical unit away from the Sun in W/m^2

    def __init__(self, max_power_w: float, efficiency: float, area_m2: float):
        """
        Initialize solar panel model.

        Args:
            max_power_w (float): Max theoretical panel power output
            efficiency (float): Panel efficiency (between 0 and 1)
            area_m2 (float): Total Area of the panel in m^2
        """
        
        self.max_power_w = max_power_w
        self.efficiency = efficiency
        self.area_m2 = area_m2

    def _get_irradiance(self, time_s: float):
        """
        Simulates the solar irradiance as a function of time for a LEO orbit.

        Args:
            param time_s: Time in seconds since the beginning of the simulation.
            return: Irradiance in W/m^2.
        """
        illuminated_fraction = 0.6  # Time exposed to the sun (~60% of the orbit)
        
        # Determine if the panel is exposed
        in_sunlight = (time_s % self.orbit_period) < (illuminated_fraction * self.orbit_period)

        if in_sunlight:
            return self.solar_constant
        else:
            return 0

    def _get_incidence_angle(self, time_s: float):
        """
        Simulates the incidence angle og the sun and the panel through out an orbit.

        Args:
            time_s: Time in seconds since the beggining of the simulation.
            return: Angle in radians.
        """
        angle_variation = np.pi / 2  # Max variaton of 90° in an orbit

        # Simulation of the sinusoidal angular variation
        return np.abs(angle_variation * np.sin(2 * np.pi * (time_s % self.orbit_period) / self.orbit_period))

    def get_power_output(self, time_s: float):
        """
        Calculates the generated power as a function of the irradiance, the and the incidence angle.

        Args:
            time_s: Time in seconds since the beggining of the simulation.
            return: Power generated in W.
        """
        G = self._get_irradiance(time_s)
        theta = self._get_incidence_angle(time_s)
        power = self.efficiency * self.area_m2 * G * np.cos(theta)

        if power > self.max_power_w:
            power = self.max_power_w

        return max(power, 0)  # In case of negative values