'''
Author: wakaba blues243134@gmail.com
Date: 2023-12-03 21:27:54
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 22:03:25
FilePath: /scripts/freq_power.py
Description: this file is used to test inference power under different frequency

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
import power.powermonitor as pm
import configparser
import socket
import threading
import traceback


# 获取配置信息
config = configparser.ConfigParser()
config.read('/home/wakaba/Desktop/scripts/config.ini')

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

# 开启功耗仪
powermonitor = pm.PowerMonitor()

# 获取不同的频点的推理的功耗开销
warmup_runs = 10
count = 50
models = subprocess.check_output('adb shell ls /data/local/tmp/tflite_model', shell=True).decode('utf-8').split('\n')
print(models)

with open(device_name + '_freq_model_cpu_power.csv', 'w') as f:
    f.write('model,cpu_freq,inference_time\n')

with open(device_name + '_freq_model_gpu_power.csv', 'w') as f:
    f.write('model,gpu_freq,inference_time\n')


def power_thread(freq, process_unit):
    HOST = '0.0.0.0'  # 监听所有接口
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print("Waiting for connection...")
        conn, addr = s.accept()
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

            with open(device_name + f'_freq_model_{process_unit}_power.csv', 'a') as f:
                f.write(f'{model},{freq},{powermonitor.power_data}\n')
            print(powermonitor.power_data)


for model in models:
    try:
        for cpu_freq in cpu_freq_list[-1]:
            fs.set_cpu_freq_by_type(-1, cpu_freq)  
            thread = threading.Thread(target=power_thread,args=(cpu_freq,'cpu',))
            thread.start()
            command = f'adb shell /data/local/tmp/label_image -m /data/local/tmp/tflite_model/{model} --warmup_runs={warmup_runs} --count={count}' 
            result = subprocess.run(command , shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            time.sleep(2)
            inference_time = result.stderr.split('\n')[-2].split()[-2]
            thread.join()
    
        fs.set_cpu_freq_by_type(-1, cpu_freq_list[-1][-1])  # cpu设置为最高频

        for gpu_freq in gpu_freq_list:
            fs.set_gpu_freq(gpu_freq, len(gpu_freq_list) - 1 - gpu_freq_list.index(gpu_freq))
            thread = threading.Thread(target=power_thread,args=(gpu_freq,'gpu',))
            thread.start()
            command = f'adb shell /data/local/tmp/label_image -m /data/local/tmp/tflite_model/{model} -g 1 --first_node=0 --last_node=9999 --warmup_runs={warmup_runs} --count={count}' 
            result = subprocess.run(command , shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            inference_time = result.stderr.split('\n')[-2].split()[-2]
            thread.join()

    except Exception as e:
        traceback.print_exc()
        print('error' + model)
        continue
 