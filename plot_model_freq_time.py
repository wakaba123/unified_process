'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-06 11:52:27
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 12:29:31
FilePath: /unified_process/plot_model_freq_time.py
Description: This file is used to plot different model's inference time under different frequency

Copyright (c) 2024 by wakaba, All Rights Reserved. 
'''

import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('pixel3freq_model_gpu.csv')

# 获取唯一的模型名称
models = df['model'].unique()

# 遍历每个模型，创建对应的图表
for model in models:
    model_data = df[df['model'] == model]
    
    # 绘制图表
    plt.figure(figsize=(10, 6))
    plt.plot(model_data['gpu_freq'], model_data['inference_time'], marker='o', label=model)
    
    # 添加标题和标签
    plt.title(f'Inference Time vs gpu Frequency for {model}')
    plt.xlabel('gpu Frequency')
    plt.ylabel('Inference Time')
    
    # 添加图例
    plt.legend()
    
    # 保存图表为图片文件
    plt.savefig(f'pics/{model}_gpu_inference_time2.png')
    
    # 显示图表（可选）
    # plt.show()

