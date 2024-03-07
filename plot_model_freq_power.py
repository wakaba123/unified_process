import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
csv_file_path = 'saved_file/a36_freq_model_gpu_power2.csv'  # 替换为你的CSV文件路径
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
    model_data['sum_power'] = model_data['power'].apply(sum)

    # 绘制子图
    axes[i].plot(model_data['gpu_freq'], model_data['sum_power'], label=model)
    axes[i].set_xlabel('freq')
    axes[i].set_ylabel('Sum of Power')
    axes[i].legend()
    axes[i].set_title(f'Sum of Power vs freq for {model}')

# 调整子图布局
plt.tight_layout()

# 保存整个图
plt.savefig('all_plots_gpu.png')

