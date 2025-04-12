import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 读取 CSV 文件
file_path = r'c:\Users\wakaba\Desktop\unified_process\findx3p_freq_idle_power.csv'
data = pd.read_csv(file_path)

# 确保数据类型为数值
data['cpu_freq'] = pd.to_numeric(data['cpu_freq'])
data['gpu_freq'] = pd.to_numeric(data['gpu_freq'])
data['power'] = pd.to_numeric(data['power'])

# 创建网格数据
cpu_freqs = sorted(data['cpu_freq'].unique())
gpu_freqs = sorted(data['gpu_freq'].unique())
cpu_grid, gpu_grid = np.meshgrid(cpu_freqs, gpu_freqs)

# 将功耗数据重塑为网格
power_grid = np.zeros_like(cpu_grid, dtype=float)
for i, gpu in enumerate(gpu_freqs):
    for j, cpu in enumerate(cpu_freqs):
        power = data[(data['cpu_freq'] == cpu) & (data['gpu_freq'] == gpu)]['power']
        power_grid[i, j] = power.values[0] if not power.empty else np.nan

# 创建三维图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面图
surf = ax.plot_surface(cpu_grid, gpu_grid, power_grid, cmap='viridis', edgecolor='none')

# 添加颜色条
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# 设置轴标签
ax.set_xlabel('CPU Frequency (Hz)')
ax.set_ylabel('GPU Frequency (Hz)')
ax.set_zlabel('Power (mW)')

# 设置标题
ax.set_title('3D Surface Plot of CPU/GPU Frequency vs Power')

# 显示图形
plt.show()