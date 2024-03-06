'''
Author: wakaba blues243134@gmail.com
Date: 2023-12-03 21:27:54
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 13:55:46
FilePath: /scripts/freq_time.py
Description: this file is used to test partition and freq setting

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''
import subprocess
import matplotlib.pyplot as plt
from datetime import datetime
import time
import numpy as np
import sys
sys.path.append('/home/wakaba/Desktop/scripts')
import basic_tools.freq_setting as fs
import configparser

config = configparser.ConfigParser()
config.read('/home/wakaba/Desktop/scripts/config.ini')

# 获得特定频率下，特定node要求下的 推理时间
def run_inference_and_get_time(cpu_freq, gpu_freq, first_node=0, last_node=999999, loop_time=5):
    fs.set_cpu_freq_by_type(-1, cpu_freq)
    fs.set_gpu_freq(gpu_freq,len(gpu_freq_list)-gpu_freq_list.index(gpu_freq)-1)
    print('setting frequency success')

    results = []
    while loop_time > 0:
        loop_time -= 1
        adb_command = f'taskset f0 adb shell "/data/local/tmp/label_image -m /data/local/tmp/mobilenet_v1_1.0_224.tflite -i /data/local/tmp/grace_hopper.bmp -l /data/local/tmp/labels.txt -g 1 --first_node={first_node} --last_node={last_node}"'
        result = subprocess.run(adb_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        inference_time = result.stderr.split('\n')[-2].split()[-2]
        results.append(float(inference_time))

    return np.mean(np.array(results))

device_name = 'pixel3'
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


#  测试每一层切割的代码
# for cpu_freq in cpu_freq_list[-1]:
#     for gpu_freq in gpu_freq_list:
#         for i in range(0, 30):
#             first_node = i 
#             last_node = 50 
#             inference_time = run_inference_and_get_time(cpu_freq, gpu_freq, first_node, last_node, loop_time=10)
#             print(cpu_freq, gpu_freq, first_node, inference_time)


# 测试cpu,gpu频点和推理时延的代码

# 获取所有的模型的频率推理时间曲线
warmup_runs = 10
count = 50
models = subprocess.check_output('adb shell ls /data/local/tmp/tflite_model', shell=True).decode('utf-8').split('\n')
print(models)

with open(device_name + '_freq_model_cpu.csv', 'w') as f:
    f.write('model,cpu_freq,inference_time\n')

with open(device_name + '_freq_model_gpu.csv', 'w') as f:
    f.write('model,gpu_freq,inference_time\n')

for model in models:
    try:
        for cpu_freq in cpu_freq_list[-1]:
            fs.set_cpu_freq_by_type(-1, cpu_freq)  # cpu设置为最高频
            command = f'adb shell /data/local/tmp/label_image -m /data/local/tmp/{model} --warmup_runs={warmup_runs} --count={count}' 
            result = subprocess.run(command , shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(2)
            inference_time = result.stderr.split('\n')[-2].split()[-2]
            with open(device_name + '_freq_model_cpu.csv', 'a') as f:
                f.write(f'{model},{cpu_freq},{inference_time}\n')
    
        fs.set_cpu_freq_by_type(-1, cpu_freq_list[-1][-1])  # cpu设置为最高频

        for gpu_freq in gpu_freq_list:
            fs.set_gpu_freq(gpu_freq, len(gpu_freq_list) - 1 - gpu_freq_list.index(gpu_freq))
            command = f'adb shell /data/local/tmp/label_image -m /data/local/tmp/{model} -g 1 --first_node=0 --last_node=9999 --warmup_runs={warmup_runs} --count={count}' 
            result = subprocess.run(command , shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            inference_time = result.stderr.split('\n')[-2].split()[-2]
            with open(device_name + '_freq_model_gpu.csv', 'a') as f:
                f.write(f'{model},{gpu_freq},{inference_time}\n')
    except:
        print(model)
        continue
 
