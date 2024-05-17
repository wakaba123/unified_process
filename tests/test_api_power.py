import configparser
import random
import sys
import time
sys.path.append('/home/wakaba/Desktop/huawei0318/unified_process')
import numpy as np
import basic_tools.freq_setting as fs
# import power.powermonitor as pm
import subprocess

config = configparser.ConfigParser()
config.read('/home/wakaba/Desktop/huawei0318/unified_process/config.ini')

device_name = 'pixel3'  # 你可以根据实际情况切换设备名称

cpu_type = fs.check_soc()
cpu_type = len(cpu_type)

freq_lists = {
    2: ['little_freq_list','big_freq_list'],
    3: ['little_freq_list', 'big_freq_list', 'super_freq_list']
}
if cpu_type in freq_lists:
    cpu_freq_list = [config.get(device_name, freq).split() for freq in freq_lists[cpu_type]]
else:
    print("Unsupported CPU type")
    raise ValueError

gpu_freq_list = config.get(device_name,'gpu_freq_list').split()

def is_sorted_ascending(lst):
    return all(lst[i] < lst[i + 1] for i in range(len(lst) - 1))

# powermonitor = pm.PowerMonitor()

fs.turn_off_on_core(0,1)
fs.turn_off_on_core(1,1)
fs.turn_off_on_core(0,0)

def test_api_power():
    power_list = []
    monitor_list = []
    for big_freq in cpu_freq_list[1][::-1]:
        print(big_freq)
        fs.set_cpu_freq_by_type(1, big_freq)
        t = 0
        power_temp = []
        # powermonitor.start()
        while t < 100:
            if t % 10 == 0:
                fs.set_cpu_freq_by_type(1, big_freq)
            try:
                voltage = int(subprocess.check_output('adb shell cat /sys/class/power_supply/battery/voltage_now',shell=True).decode('utf-8')) / 1000000
                current = int(subprocess.check_output('adb shell cat /sys/class/power_supply/battery/current_now',shell=True).decode('utf-8')) / 1000000
                print(voltage, current)
            except Exception as e:
                print('here error')
                t -= 1
                continue

            power = voltage * current
            power_temp.append(power)
            assert fs.get_cpu_freq()[1] == big_freq
            t += 1
        # powermonitor.stop()
        print(power_temp)
        # print(powermonitor.power_data)
        print(np.mean(power_temp))
        # print(np.mean(powermonitor.power_data))
        power_list.append(np.mean(power_temp))
        # monitor_list.append(np.mean(powermonitor.power_data))
        
    print('power_list',power_list)
    # print('monitor_list',monitor_list)
        
test_api_power()
    
