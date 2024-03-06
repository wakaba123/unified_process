'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-04 14:55:57
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-05 23:24:48
FilePath: /scripts/basic_tools/freq_setting.py
Description: this file is used to set freq for cpu and gpu

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''

import subprocess

def execute(cmd):
    cmds = [ 'su',cmd, 'exit']
    # cmds = [cmd, 'exit']
    obj = subprocess.Popen("adb shell", shell= True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'))
    return info[0].decode('utf-8')

# check soc architecture
def check_soc():
    position = '/sys/devices/system/cpu/cpufreq'
    cmd = f'ls {position}'
    result = execute(cmd)
    return result.split()

# set cpu governor
def set_cpu_governor(governor):
    cpu_type = check_soc()
    for policy in cpu_type:
        execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/{policy}/scaling_governor')

# set cpu frequency
def set_cpu_freq(freq):
    cpu_type = check_soc()
    policy = cpu_type
    for i in range(len(cpu_type)):
        execute(f'echo {freq[i]} > /sys/devices/system/cpu/cpufreq/{policy[i]}/scaling_min_freq')
        execute(f'echo {freq[i]} > /sys/devices/system/cpu/cpufreq/{policy[i]}/scaling_max_freq')

# set cpu frequency by type
def set_cpu_freq_by_type(type, freq): # 0 means little, 1 means big , 2 means super big
    cpu_type = check_soc()
    execute(f'echo {freq} > /sys/devices/system/cpu/cpufreq/{cpu_type[type]}/scaling_min_freq')
    execute(f'echo {freq} > /sys/devices/system/cpu/cpufreq/{cpu_type[type]}/scaling_max_freq')

# get cpu frequency
def get_cpu_freq():
    cpu_type = check_soc()
    result = []
    for policy in cpu_type:
        result.append(execute(f'cat /sys/devices/system/cpu/cpufreq/{policy}/scaling_cur_freq').replace('\n',''))
    return result

# set gpu governor
def set_gpu_governor(governor):
    execute(f'echo {governor} > /sys/class/kgsl/kgsl-3d0/devfreq/governor')

# set gpu frequency
def set_gpu_freq(freq, index):
    execute(f'echo {freq} > /sys/class/kgsl/kgsl-3d0/devfreq/min_freq')
    execute(f'echo {freq} > /sys/class/kgsl/kgsl-3d0/devfreq/max_freq')
    execute(f'echo {index} > /sys/class/kgsl/kgsl-3d0/min_pwrlevel')
    execute(f'echo {index} > /sys/class/kgsl/kgsl-3d0/max_pwrlevel')
    execute(f'echo {freq[:-6]} > /sys/class/kgsl/kgsl-3d0/max_clock_mhz')
    execute(f'echo {freq[:-6]} > /sys/class/kgsl/kgsl-3d0/min_clock_mhz')
    execute(f'echo {index} > /sys/class/kgsl/kgsl-3d0/thermal_pwrlevel')
    
# get gpu frequency
def get_gpu_freq():
    return execute(f'cat /sys/class/kgsl/kgsl-3d0/devfreq/cur_freq').replace('\n','')

