'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-04 11:58:20
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-05 23:23:24
FilePath: /unified_process/tests/test_freq_setting.py
Description: this is a test for freq_setting, including super big / big / little cpu freq setting and gpu freq setting

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''
import configparser
import random
import sys
import time
sys.path.append('/home/wakaba/Desktop/unified_process/')
import basic_tools.freq_setting as fs

config = configparser.ConfigParser()
config.read('/home/wakaba/Desktop/unified_process/config.ini')

device_name = 'findx3p'  # 你可以根据实际情况切换设备名称

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

def test_set_cpu_freq():
    fs.set_cpu_governor('performance')
    for i in range(10):
        random_freq = [random.choice(cpu_freq_list[i]) for i in range(cpu_type)]
        fs.set_cpu_freq(random_freq)
        assert fs.get_cpu_freq() == random_freq


def test_set_gpu_freq():
    fs.set_gpu_governor('userspace')
    temp = random.choice(gpu_freq_list)
    # temp = gpu_freq_list[2]
    index = gpu_freq_list.index(temp)
    print(temp)
    fs.set_gpu_freq(temp,len(gpu_freq_list) - index - 1 )
    assert fs.get_gpu_freq() == temp

