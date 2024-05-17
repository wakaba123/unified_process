import re

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # 用正则表达式替换多个空格为逗号，并添加换行符
    csv_lines = [re.sub(r'\s+', ',', line.strip()) + '\n' for line in lines]

    with open(output_file, 'w') as outfile:
        outfile.writelines(csv_lines)

# 示例用法
input_file = 'input.txt'
output_file = 'output.csv'
convert_to_csv(input_file, output_file)

