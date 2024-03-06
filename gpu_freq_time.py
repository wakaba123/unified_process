import subprocess
import matplotlib.pyplot as plt
from datetime import datetime
import time
import numpy as np

def execute(cmd):
    cmds = [ 'su',cmd, 'exit']
    # cmds = [cmd, 'exit']
    obj = subprocess.Popen("adb shell", shell= True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'))
    return info[0].decode('utf-8')

def set_cpu_governor(governor):   # for pixel 3
    execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/policy4/scaling_governor')
    execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor')

def set_gpu_governor(governor): #TODO
    execute(f'echo {governor} > /sys/class/kgsl/kgsl-3d0/devfreq/governor')

def set_gpu_freq(freq):
    print(execute(f'echo {freq} > /sys/class/kgsl/kgsl-3d0/devfreq/min_freq'))
    print(execute(f'echo {freq} > /sys/class/kgsl/kgsl-3d0/devfreq/max_freq'))

def set_thermal_freq(freq):
    execute(f'echo {freq} > /sys/devices/platform/soc/5000000.qcom,kgsl-3d0/kgsl/kgsl-3d0/thermal_pwrlevel')



big_freq_list="825600 902400 979200 1056000 1209600 1286400 1363200 1459200 1536000 1612800 1689600 1766400 1843200 1920000 1996800 2092800 2169600 2246400 2323200 2400000 2476800 2553600 2649600".split(' ')
little_freq_list = "300000 403200 480000 576000 652800 748800 825600 902400 979200 1056000 1132800 1228800 1324800 1420800 1516800 1612800 1689600 1766400".split(' ')
gpu_freq_list = "710000000 675000000 596000000 520000000 414000000 342000000 257000000".split(' ')[::-1]

model_name = "mobilenet_v1_1.0_224.tflite"

command = f"taskset f0 /data/local/tmp/benchmark_model --graph=/data/local/tmp/{model_name} --use_gpu=true"

print(command)

set_gpu_governor('performance')

results = []

i = 6 

for freq in gpu_freq_list:
    set_gpu_freq(freq)
    set_thermal_freq(i)
    i -= 1
    time.sleep(3)
    result = execute(command)
    result = result.split('\n')[-4]
    print(result)
    result = result.split(' ')[-1]
    print(result)
    results.append(int(float(result)))

print(results)
print("avg", np.mean(results))

x = [int(i) for i in gpu_freq_list]
plt.plot(x, results)

plt.xticks(rotation=45)
plt.ticklabel_format(axis='y', style='plain')
plt.grid(True)

current_time = datetime.now().strftime('%Y%m%d%H%M%S')
filename = f'gpu_{current_time}.png'

plt.savefig(filename)

