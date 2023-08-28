import re
import opencc

# 创建 OpenCC 实例
converter = opencc.OpenCC("t2s.json")

# 定义占位符和对应的日文内容的映射
placeholder_map = {}
current_placeholder = 0

def replace_japanese(match):
    global current_placeholder
    placeholder = f"__PLACEHOLDER_{current_placeholder}__"
    placeholder_map[placeholder] = match.group(0)
    current_placeholder += 1
    return placeholder

def replace_back(match):
    return placeholder_map.get(match.group(0), match.group(0))

# 读取输入文件并进行处理
with open("zhwiki-vn.xml", "r", encoding="utf-8") as input_file:
    content = input_file.read()

# 替换日文内容为占位符
pattern = re.compile(r"\{\{lang\|ja\|[\s\S]*?}}", re.MULTILINE)
content_with_placeholders = pattern.sub(replace_japanese, content)

# 进行繁简转换
converted_content = converter.convert(content_with_placeholders)

# 替换占位符回原来的日文内容
converted_content = re.sub(r"__PLACEHOLDER_\d+__", replace_back, converted_content)

# 将转换后的内容写入输出文件
with open("zhwiki-vn_simplified.xml", "w", encoding="utf-8") as output_file:
    output_file.write(converted_content)

print("繁简转换完成并已保存到zhwiki-vn_simplified.xml")
