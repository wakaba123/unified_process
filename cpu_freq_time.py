'''
Author: wakaba blues243134@gmail.com
Date: 2023-12-03 21:27:54
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-05 21:54:14
FilePath: /scripts/cpu_freq_time.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import subprocess
import matplotlib.pyplot as plt
from datetime import datetime

def execute(cmd):
    cmds = [ 'su',cmd, 'exit']
    # cmds = [cmd, 'exit']
    obj = subprocess.Popen("adb shell", shell= True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'));
    return info[0].decode('utf-8')

def set_cpu_governor(governor):   # for pixel 3
    execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/policy4/scaling_governor')
    execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor')


def set_cpu_freq(is_little, freq):
    if is_little:
        execute(f'echo {freq} > /sys/devices/system/cpu/cpufreq/policy0/scaling_setspeed')
    else:
        execute(f'echo {freq} > /sys/devices/system/cpu/cpufreq/policy4/scaling_setspeed')


big_freq_list="825600 902400 979200 1056000 1209600 1286400 1363200 1459200 1536000 1612800 1689600 1766400 1843200 1920000 1996800 2092800 2169600 2246400 2323200 2400000 2476800 2553600 2649600".split(' ')
little_freq_list = "300000 403200 480000 576000 652800 748800 825600 902400 979200 1056000 1132800 1228800 1324800 1420800 1516800 1612800 1689600 1766400".split(' ')

model_name = "mobilenet_v1_1.0_224.tflite"

command = f"taskset f0 /data/local/tmp/benchmark_model --graph=/data/local/tmp/{model_name}"

set_cpu_governor('performance')
exit(0)

results = []

for freq in big_freq_list:
    set_cpu_freq(False, freq)
    result = execute(command).split('\n')[-4]
    print(result)
    result = result.split(' ')[-1]
    print(result)
    results.append(int(float(result)))

print(results)

x = [int(i) for i in big_freq_list]
plt.plot(x, results)

plt.xticks(rotation=45)
plt.ticklabel_format(axis='y', style='plain')
plt.grid(True)

current_time = datetime.now().strftime('%Y%m%d%H%M%S')
filename = f'{current_time}.png'

plt.savefig(filename)



