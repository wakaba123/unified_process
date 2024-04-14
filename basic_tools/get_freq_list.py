import freq_setting as fs

types = fs.check_soc()

for i, type in enumerate(types):
    print(type)
    print(fs.execute('cat /sys/devices/system/cpu/cpufreq/' + type + '/scaling_available_frequencies'))
    
print('gpu')
print(fs.execute('cat /sys/class/kgsl/kgsl-3d0/devfreq/available_frequencies'))
