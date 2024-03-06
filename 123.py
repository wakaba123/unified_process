'''
Author: wakaba blues243134@gmail.com
Date: 2023-12-04 09:37:52
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-01-24 14:30:32
FilePath: /scripts/123.py
Description: 

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["Noto Serif"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题



# 两个数组的数据
data1 = ['21.014', '20.872', '28.34', '19.958', '24.643', '24.475', '23.679', '25.951', '26.144', '28.217', '19.321', '20.152', '20.18', '19.739', '19.779', '18.688', '18.459', '18.304', '18.077', '16.323', '16.147', '15.024', '12.158', '14.034', '13.284', '11.033', '9.249', '8.837', '8.869']
data2 = ['32.19', '32.595', '46.942', '42.599', '43.357', '28.524', '31.441', '48.709', '47.353', '31.997', '31.783', '31.501', '36.404', '30.333', '28.736', '26.848', '26.191', '23.844', '24.41', '21.628', '37.173', '18.32', '15.409', '15.247', '15.635', '11.665', '9.926', '9.214', '8.911']

# 将字符串转换为浮点数
data1 = [float(value) for value in data1]
data2 = [float(value) for value in data2]

# 画图
plt.plot(data1, label='Array 1')
plt.plot(data2, label='Array 2')

# 添加标签和标题
plt.xlabel('Index')
plt.ylabel('Values')
plt.title('Comparison of Arrays')

# 添加图例
plt.legend()

# 显示图形
plt.show()


# 显示图表
plt.savefig('123.png')
plt.show()
