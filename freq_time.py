'''
Author: wakaba blues243134@gmail.com
Date: 2023-12-03 21:27:54
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 13:55:46
FilePath: /unified_process/freq_time.py
Description: this file is used to test partition and freq setting

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''
import threading
import socket
import power.powermonitor as pm
import configparser
import basic_tools.freq_setting as fs
import subprocess
import matplotlib.pyplot as plt
from datetime import datetime
import time
import numpy as np
import sys
sys.path.append('/home/wakaba/Desktop/unified_process')

config = configparser.ConfigParser()
config.read('/home/wakaba/Desktop/unified_process/config.ini')

powermonitor = pm.PowerMonitor()


def evenly_select_elements(arr, num_elements):
    length = len(arr)

    if num_elements > length:
        raise ValueError(
            "Number of elements to select cannot be greater than the length of the array.")

    step = length // (num_elements - 1) if num_elements > 1 else 1
    selected_indices = [i for i in range(0, length, step)][:num_elements]

    return [arr[i] for i in selected_indices]


def power_thread(model, first_node, formatted_time,cpu_freq, gpu_freq):
    print('here in power_thread')
    HOST = '0.0.0.0'  # 监听所有接口
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except Exception as e:
            print('s bind error , waiting 10 seconds and try again')
            time.sleep(10)

        s.listen(1)
        print("Waiting for connection...")
        conn, addr = s.accept()
        inference_time = -1
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print('Received from phone:', data.decode())
                if data.decode() == "0":
                    powermonitor.start()
                if data.decode() == "1":
                    powermonitor.stop()
                if 'ms' in data.decode():
                    inference_time = data.decode()[:-3]

            with open(device_name + f'_{model}_cut_{formatted_time}.csv', 'a') as f:
                f.write(
                    f'{model},{first_node},{cpu_freq},{gpu_freq},{inference_time},{" ".join([str(i)  for i in powermonitor.power_data ])}\n')

            print(powermonitor.power_data)


device_name = 'findx3p'
cpu_type = fs.check_soc()
cpu_type = len(cpu_type)

freq_lists = {
    2: ['little_freq_list', 'big_freq_list'],
    3: ['little_freq_list', 'big_freq_list', 'super_freq_list']
}
if cpu_type in freq_lists:
    cpu_freq_list = [config.get(device_name, freq).split()
                     for freq in freq_lists[cpu_type]]
else:
    print("Unsupported CPU type")
    raise ValueError

gpu_freq_list = config.get(device_name, 'gpu_freq_list').split()

# cpu_freq_list[-1] = evenly_select_elements(cpu_freq_list[-1], 3)
# gpu_freq_list = evenly_select_elements(gpu_freq_list, 3)

model = "mobilenetv1.tflite"
warmup_runs = 10
count = 1000
current_time = datetime.now()
formatted_time = current_time.strftime("%m%d%H%M")

with open(device_name + f'_{model}_cut_{formatted_time}.csv', 'w') as f:
    f.write('model,node,inference_time,power\n')

# 测试每一层切割的代码
for cpu_freq in cpu_freq_list[-2]:
    fs.set_cpu_freq_by_type(-2, cpu_freq)
    for gpu_freq in gpu_freq_list:
        fs.set_gpu_freq(gpu_freq, len(gpu_freq_list) -
                        gpu_freq_list.index(gpu_freq)-1)
        i = 0
        while i < 30:
            first_node = i
            last_node = 50
            thread = threading.Thread(target=power_thread, args=(
                model, first_node, formatted_time, cpu_freq, gpu_freq,))
            thread.start()
            time.sleep(1)
            command = f'adb shell taskset 70 /data/local/tmp/label_image -m /data/local/tmp/tflite_model/{model} -g 1 --first_node={first_node} --last_node=9999 --warmup_runs={warmup_runs} --count={count}'
            result = subprocess.run(command, shell=True, check=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(1)
            i += 1


# 测试cpu,gpu频点和推理时延的代码

# # 获取所有的模型的频率推理时间曲线
# warmup_runs = 10
# count = 50
# models = subprocess.check_output('adb shell ls /data/local/tmp/tflite_model', shell=True).decode('utf-8').split('\n')
# print(models)

# with open(device_name + '_freq_model_cpu.csv', 'w') as f:
#     f.write('model,cpu_freq,inference_time\n')

# with open(device_name + '_freq_model_gpu.csv', 'w') as f:
#     f.write('model,gpu_freq,inference_time\n')

# for model in models:
#     try:
#         for cpu_freq in cpu_freq_list[-1]:
#             fs.set_cpu_freq_by_type(-1, cpu_freq)  # cpu设置为最高频
#             command = f'adb shell /data/local/tmp/label_image -m /data/local/tmp/{model} --warmup_runs={warmup_runs} --count={count}'
#             result = subprocess.run(command , shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             time.sleep(2)
#             inference_time = result.stderr.split('\n')[-2].split()[-2]
#             with open(device_name + '_freq_model_cpu.csv', 'a') as f:
#                 f.write(f'{model},{cpu_freq},{inference_time}\n')

#         fs.set_cpu_freq_by_type(-1, cpu_freq_list[-1][-1])  # cpu设置为最高频

#         for gpu_freq in gpu_freq_list:
#             fs.set_gpu_freq(gpu_freq, len(gpu_freq_list) - 1 - gpu_freq_list.index(gpu_freq))
#             command = f'adb shell /data/local/tmp/label_image -m /data/local/tmp/{model} -g 1 --first_node=0 --last_node=9999 --warmup_runs={warmup_runs} --count={count}'
#             result = subprocess.run(command , shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             inference_time = result.stderr.split('\n')[-2].split()[-2]
#             with open(device_name + '_freq_model_gpu.csv', 'a') as f:
#                 f.write(f'{model},{gpu_freq},{inference_time}\n')
#     except:
#         print(model)
#         continue
