import argparse
import json
import os

# 定义不合法字符到合法字符的映射
char_mapping = {
    '/': '／',
    ':': '：',
    '\\': '＼',
    '*': '＊',
    '?': '？',
    '"': '＂',
    '<': '＜',
    '>': '＞',
    '|': '｜'
}

# 定义命令行参数
parser = argparse.ArgumentParser(description='将JSON文件中的plain和markdown保存到指定文件夹')
parser.add_argument('input_json', help='输入的JSON文件')
parser.add_argument('output_folder', help='输出的文件夹')

# 解析命令行参数
args = parser.parse_args()

# 检查输出文件夹是否存在，如果不存在则创建
if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)

# 读取JSON文件
with open(args.input_json, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 遍历JSON中的每个条目
for item in data:
    title = item['title']
    pageid = item['pageid']
    plain_text = item['text']['plain']
    markdown_text = item['text']['markdown']

    # 处理标题中的不合法字符
    file_title = ''.join(char_mapping.get(c, c) for c in title)

    # 生成纯文本文件路径
    plain_filename = os.path.join(args.output_folder, f'{file_title}({pageid}).txt')
    with open(plain_filename, 'w', encoding='utf-8') as plain_file:
        plain_file.write(plain_text)

    # 生成Markdown文件路径
    markdown_filename = os.path.join(args.output_folder, f'{file_title}({pageid}).md')
    with open(markdown_filename, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_text)

print("文件保存完成！")
