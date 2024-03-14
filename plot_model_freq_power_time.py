import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
df = pd.read_csv('findx3p_freq_model_gpu_power_time.csv')

# 将第四列的每个值按空格分割，然后将结果转换为浮点数，并计算总和
df['power_sum'] = df['power'].apply(lambda x: sum(map(float, x.split())))

# 绘制图表
fig, ax1 = plt.subplots()

# 第一个 y 轴 - inference_time
color = 'tab:red'
ax1.set_xlabel('gpu_freq')
ax1.set_ylabel('inference_time', color=color)
ax1.plot(df['gpu_freq'], df['inference_time'], color=color)
print(df['inference_time'])
ax1.tick_params(axis='y', labelcolor=color)

# 第二个 y 轴 - power_sum
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('power_sum', color=color)
ax2.plot(df['gpu_freq'], df['power_sum'], color=color)
print(df['power_sum'])
ax2.tick_params(axis='y', labelcolor=color)

# 显示图表
plt.title('Inference Time and Power vs gpu Frequency')
plt.savefig('temp.png')
