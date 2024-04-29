import subprocess

def execute(cmd):
    return subprocess.check_output('hdc shell ' + f"{cmd}", shell=True).decode('utf-8')

def get_pid(process_name):
    first_pid  = execute(process_name)
    return first_pid

process = 'stress-ng'
# cpu_load = 70

# # run stress
# command = f'/data/stress-ng --cpu=8 --cpu-load={cpu_load} &'
# execute(command)

first_pid = get_pid(process)
# set real time scheduler
for i in range(first_pid, first_pid+8):
    execute(f'chrt -r -p {i} 1')






