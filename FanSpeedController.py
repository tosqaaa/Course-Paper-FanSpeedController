import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FanSpeedController:
    def __init__(self, temperature_range=(0, 101), humidity_range=(0, 101), fan_speed_range=(0, 101)):
        self._initialize_variables(temperature_range, humidity_range, fan_speed_range)
        self._initialize_rules()
        self._initialize_control_system()

    def _initialize_variables(self, temperature_range, humidity_range, fan_speed_range):
        # Define fuzzy variables
        self.temperature = ctrl.Antecedent(np.arange(*temperature_range), 'temperature')
        self.humidity = ctrl.Antecedent(np.arange(*humidity_range), 'humidity')
        self.fan_speed = ctrl.Consequent(np.arange(*fan_speed_range), 'fan_speed')

        # Define membership functions
        self._add_membership_functions(self.temperature, "temperature")
        self._add_membership_functions(self.humidity, "humidity")
        self._add_membership_functions(self.fan_speed, "fan_speed")

    def _add_membership_functions(self, variable, variable_name):
        if variable_name in ["temperature", "humidity"]:
            variable['low'] = fuzz.trimf(variable.universe, [0, 0, 50])
            variable['medium'] = fuzz.trimf(variable.universe, [30, 50, 70])
            variable['high'] = fuzz.trimf(variable.universe, [50, 100, 100])
        elif variable_name == "fan_speed":
            variable['low'] = fuzz.trimf(variable.universe, [0, 0, 50])
            variable['medium'] = fuzz.trimf(variable.universe, [30, 50, 70])
            variable['high'] = fuzz.trimf(variable.universe, [50, 100, 100])

    def _initialize_rules(self):
        # Define fuzzy rules
        self.rules = [
            ctrl.Rule(self.temperature['high'] & self.humidity['high'], self.fan_speed['high']),
            ctrl.Rule(self.temperature['medium'] & self.humidity['medium'], self.fan_speed['medium']),
            ctrl.Rule(self.temperature['low'] | self.humidity['low'], self.fan_speed['low'])
        ]

    def _initialize_control_system(self):
        # Create control system and simulation
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    def compute_fan_speed(self, temperature_value, humidity_value):
        # Input values
        self.simulation.input['temperature'] = temperature_value
        self.simulation.input['humidity'] = humidity_value

        # Perform fuzzy computation
        self.simulation.compute()

        return self.simulation.output['fan_speed']
