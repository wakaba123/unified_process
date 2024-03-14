import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取CSV文件
csv_file_path = 'saved_file/findx3p_freq_model_gpu_power_0310.csv'  # 替换为你的CSV文件路径
df = pd.read_csv(csv_file_path)

# 将 power 列中的字符串转换为数字列表
df['power'] = df['power'].apply(lambda x: [float(val) for val in x.split()])

# 计算 power 列中每个元素的和，创建新列 sum_power
df['sum_power'] = df['power'].apply(sum)

# 获取不同的 model
unique_models = df['model'].unique()
num_models = len(unique_models)

# 创建子图
fig, axes = plt.subplots(num_models, 1, figsize=(8, 4 * num_models))

# 遍历不同的 model，为每个 model 画子图
for i, model in enumerate(unique_models):
    model_data = df[df['model'] == model].copy()
    # 计算 sum_power 列
    model_data['sum_power'] = model_data['power'].apply(np.mean)
    # model_data['sum_power2'] = model_data.apply(lambda row: row['sum_power'] - row['inference_time'] / 1000 * 900 * 120, axis=1)


    # 第一个 y 轴 - inference_time
    color = 'tab:red'
    axes[i].set_xlabel('gpu_freq')
    axes[i].set_ylabel('inference_time', color=color)
    axes[i].plot(model_data['gpu_freq'], model_data['inference_time'], color=color, label='latency')
    axes[i].tick_params(axis='y', labelcolor=color)

    # 第二个 y 轴 - power_sum
    ax2 = axes[i].twinx()
    color = 'tab:blue'
    ax2.set_ylabel('power_sum', color=color)
    ax2.plot(model_data['gpu_freq'], model_data['sum_power'], color=color,label='energy')
    ax2.tick_params(axis='y', labelcolor=color)

    axes[i].set_title(f'latency/energy vs freq for {model}')
    

# 调整子图布局
plt.tight_layout()

# 保存整个图
plt.savefig('findx3p_gpu.png')

