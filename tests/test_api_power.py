import configparser
import random
import sys
import time
sys.path.append('/home/wakaba/Desktop/unified_process/')
import numpy as np
import basic_tools.freq_setting as fs

config = configparser.ConfigParser()
config.read('/home/wakaba/Desktop/unified_process/config.ini')

device_name = 'k20p'  # 你可以根据实际情况切换设备名称

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

def test_api_power():
    power_list = []
    for big_freq in cpu_freq_list[1]:
        print(big_freq)
        fs.set_cpu_freq_by_type(1, big_freq)
        t = 0
        power_temp = []
        while t < 20:
            voltage = int(fs.execute('cat /sys/class/power_supply/battery/voltage_now')) / 1000000
            current = int(fs.execute('cat /sys/class/power_supply/battery/current_now')) / 1000000
            power = voltage * current
            power_temp.append(power)
            t += 1
        print(power_temp)
        power_list.append(np.mean(power_temp))
        print(np.mean(power_temp))
    print(power_list)
    assert is_sorted_ascending(power_list)
        
test_api_power()
    
