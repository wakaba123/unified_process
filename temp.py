'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-26 10:58:44
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-26 15:21:24
FilePath: /unified_process/temp.py
Description: 

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''
import matplotlib.pyplot as plt

# 线程数
threads = [1, 2, 3, 4, 5, 6, 7, 8]
# 推理时间
inference_times = [131.737, 259.317, 387.988, 517.436, 637.589, 765.137, 900.225, 1036.5]

# 创建图像
plt.figure(figsize=(10, 6))
# 绘制线条图
plt.plot(threads, inference_times, marker='o', linestyle='-', color='r')

# 添加标题和轴标签
plt.title('Thread Count vs. Inference Time on Pixel 4')
plt.xlabel('Number of Threads')
plt.ylabel('Inference Time (ms)')

# 显示网格
plt.grid(True)
# 添加图例
plt.legend(['InceptionV4'])

# 显示图像
plt.show()
