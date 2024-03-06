import threading
import subprocess
import time

def execute(cmd):
    cmds = ['su','export LD_LIBRARY_PATH=/data/local/tmp/lib:$LD_LIBRARY_PATH', cmd, 'exit']
    obj = subprocess.Popen("adb shell", shell=True, stdin=subprocess.PIPE)
    obj.stdin.write(("\n".join(cmds) + "\n").encode('utf-8'))
    obj.stdin.close()
    obj.communicate()
    return 1

def execute_in_thread(command):
    t1 = time.time()
    execute(command)
    t2 = time.time()
    print(f"Execution time for command '{command}': {t2 - t1} seconds")

# 示例用法：启动多条线程执行命令
num_threads = 6
use_gpu = 'false'
command = f'taskset 01 /data/local/tmp/minimal /data/local/tmp/models/mobilenet_v1_1.0_224.tflite 1 1'

threads = []
t1 = time.time()
for _ in range(num_threads):
    thread = threading.Thread(target=execute_in_thread, args=(command,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

t2 = time.time()
print(t2-t1)