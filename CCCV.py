import pybamm
import numpy as np
import matplotlib.pyplot as plt

# 定义电池模型
model = pybamm.lithium_ion.SPM()

# 定义CCCV充电协议
experiment = pybamm.Experiment([
    ('Charge at 1 C until 4.2 V',
     'Hold at 4.2 V until 50 mA'),
    'Rest for 1 hour'
])

# 创建仿真器对象
sim = pybamm.Simulation(model, experiment=experiment)

# 运行仿真
sim.solve()

# 绘制结果
sim.plot()
