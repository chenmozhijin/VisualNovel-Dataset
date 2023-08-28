import xml.etree.ElementTree as ET
import opencc
import re

# 创建简繁转换器实例
converter = opencc.OpenCC("t2s.json")  # t2s.json 是简体化配置文件

# 读取维基百科的XML文件
input_file = "zhwiki.xml"
output_file = "zhwiki_simplified.xml"

tree = ET.parse(input_file)
root = tree.getroot()

# 正则表达式匹配日文内容的标记
ja_pattern = re.compile(r"{{lang\|ja\|(.*?)}}")

# 遍历XML文档，将繁体字转换为简体，但跳过日文内容的标记
for element in root.iter():
    if element.text:  # 如果文本内容不为空
        if not any(child.tag == "lang" and child.attrib.get("lang") == "ja" for child in element):
            # 如果没有日文内容的标记，则进行转换
            element.text = converter.convert(element.text)
        else:
            # 如果存在日文内容的标记，则跳过转换
            ja_match = ja_pattern.search(element.text)
            if ja_match:
                ja_content = ja_match.group(1)
                element.text = element.text.replace(ja_content, converter.convert(ja_content))

# 将转换后的XML写入新文件
tree.write(output_file, encoding="utf-8", xml_declaration=True)
