'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-05 21:18:51
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-05 21:24:07
FilePath: /scripts/output_tflite.py
Description: this file is used to output tflite structure

Copyright (c) 2024 by wakaba All Rights Reserved. 
'''
import tensorflow as tf

# 加载TFLite模型
interpreter = tf.lite.Interpreter(model_path="/home/wakaba/Desktop/tflite_model/EfficientNet.tflite")
interpreter.allocate_tensors()

# 获取TFLite模型的图定义
tflite_graph_def = interpreter.get_tensor_details()

# 打印TFLite模型的基本信息
for node in tflite_graph_def:
    print("Node Name:", node['name'])
    print("Node Shape:", node['shape'])
    print("Node Type:", node['dtype'])
    print("--------------")
