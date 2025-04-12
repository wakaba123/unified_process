'''
Author: wakaba blues243134@gmail.com
Date: 2023-12-03 21:27:54
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 22:03:25
FilePath: /unified_process/freq_power.py
Description: this file is used to test idle power under different frequency

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''
import subprocess
import time
import sys
sys.path.append(r'C:\Users\wakaba\Desktop\unified_process')
import basic_tools.freq_setting as fs
import power.powermonitor as pm
import configparser
import socket
import threading
import traceback

# 获取配置信息
config = configparser.ConfigParser()
config.read(r'C:\Users\wakaba\Desktop\unified_process\config.ini')

device_name = 'findx3p'
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


def power_thread(cpu_freq, gpu_freq):
    print(f'Starting power measurement for CPU freq: {cpu_freq} and GPU freq: {gpu_freq}')
    
    # 开始功耗统计
    powermonitor.start()
    time.sleep(5)  # 空闲状态持续5秒
    powermonitor.stop()
    
    # 计算平均功耗
    avg_power = sum(powermonitor.power_data) / len(powermonitor.power_data)
    
    # 写入 CSV 文件
    with open(device_name + '_freq_idle_power.csv', 'a') as f:
        f.write(f'{cpu_freq},{gpu_freq},{avg_power}\n')
    
    print(f'Power measurement finished for CPU freq: {cpu_freq}, GPU freq: {gpu_freq}, Power: {avg_power}')


def read_ftrace(cpu_freq, gpu_freq):
    """
    从 trace_pipe 中读取 5 秒的 ftrace 数据并保存到文件
    """
    ftrace_file = f'ftrace_cpu_{cpu_freq}_gpu_{gpu_freq}.txt'
    try:
        with open(ftrace_file, 'w') as f:
            # 打开 trace_pipe 并读取 5 秒的数据
            with subprocess.Popen("adb shell atrace gfx -t 5", 
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                start_time = time.time()
                while time.time() - start_time < 7:  # 读取 5 秒
                    line = proc.stdout.readline()

                    # print(line)
                    if not line:
                        break
                    f.write(line)
        print(f"Saved ftrace data to {ftrace_file}")
    except Exception as e:
        print(f"Error while reading ftrace: {e}")


try:
    # CPU 和 GPU 频点组合空闲功耗统计
    with open(device_name + '_freq_idle_power.csv', 'w') as f:
        f.write('cpu_freq,gpu_freq,power\n')  # 写入表头

    fs.set_cpu_freq_by_type(0, cpu_freq_list[0][-1])  # 设置小核频率为最大值

    # 获取 com.ss.android.ugc.aweme 的 PID 并绑定到大核
    aweme_pid = subprocess.check_output(
        "adb shell pidof com.ss.android.ugc.aweme", shell=True
    ).decode().strip()
    subprocess.run(f"adb shell taskset -p 70 {aweme_pid}", shell=True)
    print(f"Bound com.ss.android.ugc.aweme (PID: {aweme_pid}) to big cores")

    # 获取 surfaceFlinger 的 PID 并绑定到大核
    surfaceflinger_pid = subprocess.check_output(
        "adb shell pidof surfaceflinger", shell=True
    ).decode().strip()
    subprocess.run(f"adb shell taskset -p 70 {surfaceflinger_pid}", shell=True)
    print(f"Bound surfaceFlinger (PID: {surfaceflinger_pid}) to big cores")

    for cpu_freq in cpu_freq_list[1]:
        fs.set_cpu_freq_by_type(1, cpu_freq)
        for gpu_freq in gpu_freq_list:
            fs.set_gpu_freq(gpu_freq, len(gpu_freq_list) - 1 - gpu_freq_list.index(gpu_freq))
            
            # 开始读取 ftrace 数据
            ftrace_thread = threading.Thread(target=read_ftrace, args=(cpu_freq, gpu_freq))
            ftrace_thread.start()

            # 直接调用 power_thread 进行功耗统计
            power_thread(cpu_freq, gpu_freq)

            # 等待 ftrace 线程完成
            ftrace_thread.join()

except Exception as e:
    traceback.print_exc()
    print('Error occurred during idle power measurement')

