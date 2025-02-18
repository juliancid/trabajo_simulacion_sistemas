import numpy as np

class SolarPanel:

    orbit_period = 5400 # LEO Orbit period in seconds (~90 min)
    solar_constant = 1361 # W/m^2

    def __init__(self, max_power_w: float, efficiency: float, area_m2: float):
        """
        Inicializa el modelo del panel solar.

        :param max_power_w: Potencia máxima teórica del panel en W.
        :param efficiency: Eficiencia del panel (0 a 1).
        :param area_m2: Área del panel en metros cuadrados.
        """
        self.max_power_w = max_power_w
        self.efficiency = efficiency
        self.area_m2 = area_m2

    def _get_irradiance(self, time_s: float) -> float:
        """
        Simulates the solar irradiance as a function of time for a LEO orbit.

        :param time_s: Tiempo en segundos desde el inicio de la simulación.
        :return: Irradiancia en W/m².
        """
        illuminated_fraction = 0.6  # Tiempo en el que está al sol (~60% de la órbita)
        
        # Determinar si está en el lado iluminado
        in_sunlight = (time_s % SolarPanel.orbit_period) < (illuminated_fraction * SolarPanel.orbit_period)

        if in_sunlight:
            return SolarPanel.solar_constant
        else:
            return 0

    def _get_incidence_angle(self, time_s: float) -> float:
        """
        Simula el ángulo de incidencia del sol en el panel a lo largo de la órbita.

        :param time_s: Tiempo en segundos desde el inicio de la simulación.
        :return: Ángulo en radianes.
        """
        angle_variation = np.pi / 2  # Variación máxima de 90° en una órbita

        # Simulación de variación angular sinusoidal
        return np.abs(angle_variation * np.sin(2 * np.pi * (time_s % SolarPanel.orbit_period) / SolarPanel.orbit_period))

    def get_power_output(self, time_s: float) -> float:
        """
        Calcula la potencia generada por el panel en función de la irradiancia y el ángulo de incidencia.

        :param time_s: Tiempo en segundos desde el inicio de la simulación.
        :return: Potencia generada en W.
        """
        G = self._get_irradiance(time_s)  # Obtener irradiancia
        theta = self._get_incidence_angle(time_s)  # Ángulo de incidencia
        power = self.efficiency * self.area_m2 * G * np.cos(theta)
        return max(power, 0)  # Evitar valores negativos

