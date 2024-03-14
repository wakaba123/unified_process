import sys
sys.path.append('/home/wakaba/Desktop/unified_process')
import power.powermonitor as pm
import time
import numpy as np

a = pm.PowerMonitor()
a.start()
for i in range(50):
    time.sleep(1)
a.stop()
print(a.power_data)
print(np.mean(a.power_data))


