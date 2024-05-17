import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('result.csv')

def cal_power(freq,state0,state1,state2,state3):
    a0 = 1
    a1 = 0.75
    a2 = 0.50
    a3 = 0.25
    return freq*freq*freq * (a0 * state0 + a1*state1 + a2*state2 + a3*state3)

def get_power_by_core(cpu):
    df = df[df['cpu'] == cpu]
    total = 0
    for index, row in df.iterrows():
        total += cal_power(row['freq'],row['state0'],row['state1'],row['state2'],row['state3'])
    return total

for i in range(8):
    total = 0
    total += get_power_by_core(i)
    print(total)

        

