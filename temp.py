import matplotlib.pyplot as plt
import numpy as np

# 数据
run_order = [i for i in range(0, 31)]  # Run Order 列
avg_ms = [1.580, 0.999, 2.701, 1.047, 2.560, 1.221, 5.079, 0.453, 2.497, 0.640, 
          4.975, 0.204, 2.513, 0.373, 5.062, 0.369, 5.101, 0.376, 5.067, 0.373, 
          5.066, 0.367, 5.083, 0.128, 2.955, 0.225, 7.354, 0.038, 0.559, 0.001, 0.004]  # avg ms 列
print(np.sum(np.array(avg_ms)))

avg_ms_gpu = [0.087, 0.180, 0.297, 0.181, 0.264, 0.179, 0.505, 0.090, 0.262, 0.094,
              0.507, 0.057, 0.286, 0.057, 0.540, 0.057, 0.545, 0.059, 0.558, 0.059,
              0.553, 0.057, 0.552, 0.032, 0.344, 0.038, 0.694, 0.022, 0.114, 0.012]  # avg ms 列

print(np.sum(np.array(avg_ms_gpu)))
# 绘制曲线图
plt.plot(avg_ms, marker='o', linestyle='-', color='b',label='cpu')
plt.plot(avg_ms_gpu, marker='o', linestyle='-', color='r',label='gpu')
plt.title('Mobilenet_1.0_224(float) Operator-wise Profiling Avg Time')
plt.xlabel('Run Order')
plt.ylabel('Avg Time (ms)')
plt.legend()
plt.grid(True)
plt.show()
