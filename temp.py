from datetime import datetime

# 获取当前时间
current_time = datetime.now()

# 格式化为指定字符串
formatted_time = current_time.strftime("%m%d%H%M")

print("当前时间的字符串格式为:", formatted_time)
