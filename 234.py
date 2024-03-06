'''
Author: wakaba blues243134@gmail.com
Date: 2023-12-04 09:37:52
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-01-24 14:10:26
FilePath: /scripts/234.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["Noto Serif"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题


# 提供的数据
data = [
    (1, 20740, 7.3),
    (2, 37021, 15.08),
    (3, 61232, 22.98),
    (4, 69393, 31.98),
    (5, 79260, 42.19),
    (6, 104659, 50.24)
]

# 将数据分离为三个列表
x_values = [entry[0] for entry in data]
y1_values = [entry[1]/1000 for entry in data]
y2_values = [entry[2] for entry in data]
y3_values = []

for i in range(len(data)):
    y3_values.append(y1_values[i] * (i+1))


# 绘制折线图
plt.plot(x_values, y1_values,marker='o', label='execution time')
# plt.plot(x_values, y2_values,marker='o', label='total_time')
# plt.plot(x_values, y3_values,marker='o', label='expected_time')

# 添加标题和标签
plt.title('Data Visualization')
plt.xlabel('model_num')
plt.ylabel('time(ms)')

# 添加图例
plt.legend()

# 显示图表
plt.savefig('123.png')
plt.show()
