import json
import os
import argparse

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description='合并多个JSON文件')

# 添加输入和输出文件路径的参数
parser.add_argument('input_folder', help='输入JSON文件夹路径')
parser.add_argument('output_file', help='输出合并后的JSON文件路径')

# 解析命令行参数
args = parser.parse_args()

# 使用命令行参数中指定的路径
input_folder = args.input_folder
output_file = args.output_file

# 创建一个空的数据列表
merged_data = []

# 遍历JSON文件夹中的所有文件
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        merged_data.extend(data)

# 将合并后的数据写入输出文件
with open(output_file, 'w', encoding='utf-8') as output_json:
    json.dump(merged_data, output_json, ensure_ascii=False, indent=4)

print(f'合并后的JSON文件已保存为 {output_file}')
