import subprocess

def execute(cmd):
    return subprocess.check_output('hdc shell ' + f"{cmd}", shell=True).decode('utf-8')

def get_fps(view='composer'):
    cmd = f'hidumper -s RenderService -a "f{view} fps"'
    output = execute(cmd)
    timestamps = output.split('\n')
    last_timestamp = timestamps[-1]
    count = 0
    for timestamp in timestamps[::-1]:
        if last_timestamp - timestamp  > 1e9:
            break
        count += 1
    return count

def set_freq(type, freq): # 0 means little , 1 means middle , 2 means big
    execute(f'echo {freq} > /sys/devices/system/cpu/cpufreq/policy{type}/scaling_min_freq')
    execute(f'echo {freq} > /sys/devices/system/cpu/cpufreq/policy{type}/scaling_max_freq')
    assert execute(f'cat /sys/devices/system/cpu/cpufreq/policy{type}/scaling_cur_freq') == freq

def get_view():
    view = ''
    return view

super_big_list = ''
big_freq_list = ''
little_freq_list = ''
target_fps = 24

for super_freq in super_big_list[::-1]:
    set_freq(2, super_freq)
    for big_freq in big_freq_list[::-1]:
        set_freq(1, big_freq)
        for little_freq in little_freq_list[::-1]:
            set_freq(0, little_freq)

            ## here add stress

            t = 0
            fps_miss_count = 0
            flag = 0

            while t < 20:
                fps = get_fps()

                if fps < target_fps:
                    fps_miss_count += 1
            
                if fps_miss_count >= 5:
                    flag = 1
                    print('too many jank frames!')
                    print(f'current freq is {super_freq}, {big_freq}, {little_freq}')
                    break 

                t += 1


