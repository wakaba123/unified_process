import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('findx3p_mobilenetv1.tflite_cut_03110926.csv')

df['power'] = df['power'].apply(lambda x: [float(val) for val in x.split()])
df['power_sum'] = df['power'].apply(sum)

# 提取唯一的CPU频率和GPU频率
cpu_freq_list = df['cpu_freq'].unique()
gpu_freq_list = df['gpu_freq'].unique()

# 循环遍历CPU频率和GPU频率，分别绘制图表
for cpu_freq in cpu_freq_list:
    for gpu_freq in gpu_freq_list:
        # 选择相应频率的数据
        subset = df[(df['cpu_freq'] == cpu_freq) & (df['gpu_freq'] == gpu_freq)]
        # 创建图表

        print(gpu_freq)
        # 第一个Y轴，推理时间
        if str(gpu_freq) == '840000000':
            color = 'tab:red'
            label='max'
        else:
            color = 'tab:blue'
            label='min'
        
        
        plt.plot(subset['node'], subset['power_sum'], color=color, label=label)

plt.legend()
plt.tick_params(axis='y', labelcolor=color)

plt.savefig('temp.png')
