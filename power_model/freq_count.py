import pandas as pd

cpu_freq_data = pd.read_csv('cpu_freq.csv')
df = cpu_freq_data
df['start'] = df['startNS']
df['end'] = df['startNS'] + df['dur']
cpu_freq_data = df[['cpu','start', 'end', 'value','dur']]

cpu_idle_data = pd.read_csv('cpu_idle.csv')
df = cpu_idle_data
df['start'] = df['startNS']
df['end'] = df['startNS'] + df['dur']
cpu_idle_data = df[['cpu','start', 'end', 'value','dur']]

little_freq = [100,200,300]
big_freq= [] 
super_freq = []
freq_lists = [little_freq, big_freq, super_freq]
policy = [[0,1],[2,3,4],[5,6,7]]

results = {}
freq_time_dict = {}
f = open('result.csv','w') 
f.write('cpu,freq,total_time,state0,state1,state2,state3\n')

for i in range(8):
    cpu_freq_data_temp = cpu_freq_data[cpu_freq_data['cpu'] == i].sort_values(by='start')
    cpu_idle_data_temp = cpu_idle_data[cpu_idle_data['cpu'] == i].sort_values(by='start')

    if i in policy[0]:
        frequencies = freq_lists[0]
    if i in policy[1]:
        frequencies = freq_lists[1]
    if i in policy[2]:
        frequencies = freq_lists[2]

    print(frequencies)
    for frequency in frequencies:
        filtered_cpu_freq_data = cpu_freq_data_temp[cpu_freq_data_temp['value'] == frequency]
        if filtered_cpu_freq_data.empty:
            total_time_frequency = 0
        else:
            total_time_frequency = filtered_cpu_freq_data['dur'].sum()
        freq_time_dict[frequency] = total_time_frequency

    print(i, freq_time_dict)

    results = {}

    for frequency in frequencies:
        filtered_cpu_freq_data = cpu_freq_data_temp[cpu_freq_data_temp['value'] == frequency]
        cpu_state_occupancy = {cpu_state: 0 for cpu_state in range(4)}

        for index, row in filtered_cpu_freq_data.iterrows():
            freq_start = row['start']
            freq_end = row['end']

            state_temp = 0
            while True:
                if state_temp >= len(cpu_idle_data_temp):
                    break
                
                state_start = cpu_idle_data.iloc[state_temp]['start']
                state_end = cpu_idle_data.iloc[state_temp]['end']
                state = cpu_idle_data.iloc[state_temp]['value']

                if state_start > freq_end: # 已经离开该区间
                    break

                if state_end < freq_start: # 还没到该区间
                    state_temp += 1
                    continue

                if state_start >= freq_start and state_end <= freq_end :
                    cpu_state_occupancy[state] += state_end - state_start

                # freq完全在state里面
                if state_start <= freq_start and state_end >= freq_end:
                    cpu_state_occupancy[state] += (freq_end - freq_start)

                # state左边一部分在外面
                if state_start < freq_start and state_end <= freq_end and state_end >= freq_start:
                    cpu_state_occupancy[state] += (state_end - freq_start)

                #state 右边一部分在外面
                if state_start >= freq_start and state_start < freq_end and state_end > freq_end:
                    cpu_state_occupancy[state] += (freq_end - state_start)

                state_temp += 1

        results[frequency] = cpu_state_occupancy
        f.write(f'{i},{frequency},{freq_time_dict[frequency]},{cpu_state_occupancy[0]},{cpu_state_occupancy[1]},{cpu_state_occupancy[2]},{cpu_state_occupancy[3]}\n')

    print(i, results)
print('finished')