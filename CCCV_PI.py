import pybamm
import numpy as np
import matplotlib.pyplot as plt

model = pybamm.lithium_ion.SPM()

class PIController:
    def __init__(self, Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
        self.integral = 0

    def update(self, error, dt):
        self.integral += error * dt
        output = self.Kp * error + self.Ki * self.integral
        return output

I_set = 1  # Constant current (in Amperes)
V_max = 4.2  # Maximum voltage (in Volts)
current_cutoff = 0.05  # Cutoff current (in Amperes)
Kp = 0.1  # Proportional gain
Ki = 0.01  # Integral gain

controller = PIController(Kp, Ki)

# Initialize solver
solver = pybamm.CasadiSolver()

# Initialize variables
current = I_set
voltage = 0
initial_soc = 0.2
current_output = []
voltage_output = []
time_output = []
# Create simulation
sim = pybamm.Simulation(model, solver=solver)
param = pybamm.ParameterValues("Chen2020")
# 电流函数
# def external_current(t, voltage, current, controller, I_set, V_max):
#     error = I_set - current
#     current += controller.update(error, 1)  # dt = 1 second for simplicity
#     # Calculate error and update PI controller
#     if voltage <= V_max:
#         error = I_set - current
#         current += controller.update(error, 1)
#
#     # Switch to CV mode if voltage exceeds V_max
#     else:
#         error = V_max - voltage
#         current += controller.update(error, 1)
#     # Stop if current is below cutoff
#     if current < current_cutoff:
#         current = 0
#     return current

# Define time step
dt = 1  # Time step in seconds

# Run simulation for a maximum of 3600 seconds
for t in np.arange(0, 3600, dt):
    # Update model with current value
    param.update({"Current function [A]": current})

    # Solve for one time step
    solution = sim.step(dt=dt)

    # Get the voltage and time
    voltage = solution["Terminal voltage [V]"].entries[-1]
    time = solution.t[-1]

    # Store outputs
    current_output.append(current)
    voltage_output.append(voltage)
    time_output.append(time)

    # Calculate error and update PI controller
    error = I_set - current
    current += controller.update(error, dt)

    # Calculate error and update PI controller
    if voltage <= V_max:
        error = I_set - current
        current += controller.update(error, 1)

    # Switch to CV mode if voltage exceeds V_max
    else:
        error = V_max - voltage
        current += controller.update(error, 1)
    # Stop if current is below cutoff
    if current < current_cutoff:
        current = 0

plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(time_output, current_output, label='Current (A)')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time_output, voltage_output, label='Voltage (V)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()

plt.tight_layout()
plt.show()
