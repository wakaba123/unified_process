import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# 读取 CSV 文件
df = pd.read_csv('temp.csv')
# df = pd.read_csv('findx3p_mobilenetv1.tflite_cut_03101950.csv')

# 将第四列的每个值按空格分割，然后将结果转换为浮点数，并计算总和

df['power'] = df['power'].apply(lambda x: [float(val) for val in x.split()])
df['power_avg'] = df['power'].apply(sum)

# 绘制图表
fig, ax1 = plt.subplots()

# 第一个 y 轴 - inference_time
color = 'tab:red'
ax1.set_xlabel('node')
ax1.set_ylabel('inference_time', color=color)
ax1.plot(df['node'], df['inference_time'], color=color)
print(df['inference_time'])
ax1.tick_params(axis='y', labelcolor=color)

# 第二个 y 轴 - power_sum
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('power_sum', color=color)
ax2.plot(df['node'], df['power_avg'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# 显示图表
plt.title('Inference Time and Power vs cutting node')

current_time = datetime.now()
formatted_time = current_time.strftime("%m%d%H%M")
plt.savefig(f'cut_{formatted_time}.png')

