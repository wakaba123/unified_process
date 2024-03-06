import matplotlib.pyplot as plt
import subprocess
from matplotlib.animation import FuncAnimation


def execute(cmd):
    cmds = [ 'su',cmd, 'exit']
    # cmds = [cmd, 'exit']
    obj = subprocess.Popen("adb shell", shell= True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'));
    return info[0].decode('utf-8')

def execute_bg(cmd):
    obj = subprocess.Popen(f"adb shell '{cmd}'",shell=True)


def get_top_head():
    output = execute('top -bn1')
    return output

def parse_top_output(output):
    lines = output.split('\n')
    line = lines[1]
    mem_info = list(filter(None, line.split(' ')))
    free_memory = int(mem_info[5][:-1])  # Free memory value is in the 6th position
    line = lines[3]
    # Splitting the line by spaces and filtering out empty strings
    cpu_info = list(filter(None, line.split(' ')))
    idle_cpu = float(cpu_info[4][:-5])  # Idle CPU percentage is in the 8th position

    # Calculate total CPU usage
    total_cpu_usage = 800 - idle_cpu  # Assuming 800% is the full capacity for an 8-core CPU

    return int(total_cpu_usage), int(free_memory)

def get_gpu_busy_percentage():
    gpu_busy = execute('cat /sys/class/kgsl/kgsl-3d0/gpu_busy_percentage')
    return int(gpu_busy[:-2])

def get_gpu_clock():
    gpu_clock = execute('cat /sys/class/kgsl/kgsl-3d0/clock_mhz')
    return int(gpu_clock[:-1])

def get_cpu_clock():
    super_big_clock = execute('cat /sys/devices/system/cpu/cpufreq/policy7/scaling_cur_freq')
    big_clock = execute('cat /sys/devices/system/cpu/cpufreq/policy4/scaling_cur_freq')
    little_clock = execute('cat /sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq')
    try:
        return int(super_big_clock[:-1]), int(big_clock[:-1]), int(little_clock[:-1])
    except:
        return 0, int(big_clock[:-1]), int(little_clock[:-1])


def set_governor(governor):
    execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/policy4/scaling_governor')
    execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/policy7/scaling_governor')
    execute(f'echo {governor} > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor')

set_governor('schedutil')

# set_governor('performance')

cpu_usages = []
ava_mems = []
gpu_busys = []
gpu_clocks = []
super_big_clocks = []
big_clocks = []
little_clocks = []

# Create subplots
fig, axs = plt.subplots(7, 1, figsize=(10, 15))

def update(frame):
    # cpu_usage, ava_mem = parse_top_output(get_top_head())
    # gpu_busy = get_gpu_busy_percentage()
    gpu_clock = get_gpu_clock()
    super_big_clock , big_clock, little_clock = get_cpu_clock()

    # cpu_usages.append(cpu_usage)
    # ava_mems.append(ava_mem)
    # gpu_busys.append(gpu_busy)
    gpu_clocks.append(gpu_clock)
    super_big_clocks.append(super_big_clock)
    big_clocks.append(big_clock)
    little_clocks.append(little_clock)

    # Set data for each subplot
    # axs[0].clear()
    # axs[0].plot(cpu_usages, label='CPU Usage')
    # axs[0].legend(loc='upper left')
    # axs[0].set_title('CPU Usage')

    # axs[1].clear()
    # axs[1].plot(ava_mems, label='Available Memory')
    # axs[1].legend(loc='upper left')
    # axs[1].set_title('Available Memory')

    # axs[2].clear()
    # axs[2].plot(gpu_busys, label='GPU Busy Percentage')
    # axs[2].legend(loc='upper left')
    # axs[2].set_title('GPU Busy Percentage')

    axs[3].clear()
    axs[3].plot(gpu_clocks, label='GPU Clock')
    axs[3].legend(loc='upper left')
    axs[3].set_title('GPU Clock')

    axs[4].clear()
    axs[4].plot(super_big_clocks, label='Super Big Core Clock')
    axs[4].legend(loc='upper left')
    axs[4].set_title('Big Core Clock')

    axs[5].clear()
    axs[5].plot(big_clocks, label='Big Core Clock')
    axs[5].legend(loc='upper left')
    axs[5].set_title('Little Core Clock')

    axs[6].clear()
    axs[6].plot(little_clocks, label='Little Core Clock')
    axs[6].legend(loc='upper left')
    axs[6].set_title('Little Core Clock')

    # Adjust layout
    plt.tight_layout()

    # print(cpu_usage, ava_mem, gpu_busy, gpu_clock, big_clock, little_clock)

ani = FuncAnimation(fig, update, interval=1000)
plt.show()