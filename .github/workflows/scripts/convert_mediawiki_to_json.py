import mwparserfromhell as mwparser
import json
import sys
import re
import os

def preprocess_text(text, input_file_name):
    base_file_name = os.path.splitext(os.path.basename(input_file_name))[0]
    text = text.replace("'''{{PAGENAME}}'''", base_file_name).replace("{{PAGENAME}}", base_file_name)\
    
    print(f"{input_file_name}转换进度1/40")
    text = re.sub(r"\{\{clear\}\}|\{\{剧透\}\}|\{\{剧透提醒\}\}|<big>|</big>|<small>|</small>|'''''|'''|''|<br />|<br/>|<br[^>]*>|<del[^>]*>|</del>|<s[^>]*>|</s>|<span[^>]*>|</span>|<ins[^>]*>|</ins>|<u[^>]*>|</u>|<poem[^>]*>|</poem>|<div[^>]*>|</div>|\[\[File:[^\]]*\]\]|\[\[文件:[^\]]*\]\]|\[\[[Ii]mage:[^\]]*\]\]|\{\{#tag:div\|<img[^}{]*\}\}|==画廊==|== 注释 ==|\{\{#ifexpr.*\n.*\n.*\}\}\}\}", r'', text)#匹配并删除#|<code>|</code>|<nowiki>|</nowiki>|<pre>|</pre>

    text = re.sub(r'<ref[^>]*>([^<]*)</ref>', r'（注：\1）', text)#匹配注脚

    text = re.sub(r'\[(https?://[^ \]]+) ([^\]]+)\]', r'\2：\1', text)#匹配本站外文字链接（显示替换文字与目标页面的页面标题不同）

    text = re.sub(r'\{\{dead\|([^}]+)\}\}', r'\1', text)#匹配dead
    print(f"{input_file_name}转换进度5/40")
    text = re.sub(r'\[\[(?!File:)(?!文件:)(?![Ii]mage:)(?!#)[^[}{\]|]*\|(?!\*)([^}{[\]]*)\]\]', r'\1', text)#匹配[[实际页面|显示文字]]]

    text = re.sub(r'\{\{[Rr]uby\|([^|}{]+)\|([^|}{]+)[|jaenzh]*\}\}', r'\1', text) #匹配[Rr]uby

    text = re.sub(r'\[\[(?!File:)(?!文件:)(?![Ii]mage:)(?!#)[^[}{\]|]*\|(?!\*)([^}{[\]]*)\]\]', r'\1', text)#匹配[[实际页面|显示文字]]] for {{lang|ja|「[[致永远之星|{{ruby|永遠|とわ}}の星へ]]」}}

    text = re.sub(r'\{\{[Ff]ont[^}{]*\|((?:[^}{]|\n)+)\}\}', r'\1', text)#匹配[Ff]ont

    text = re.sub(r'\{\{[Ll]j\|((?:[^}{]|\n)+)\}\}', r'\1', text)#匹配[Ll]j
    print(f"{input_file_name}转换进度10/40")
    text = re.sub(r'\{\{[Cc]olor\|[^|}{]+\|((?:[^}{]+)|\n)\}\}', r'\1', text)#匹配color

    text = re.sub(r'\{\{coloredlink\|[^|}{]+\|([^}{]+)\}\}', r'\1', text)#匹配coloredlink

    text = re.sub(r'\{\{[Ll]ang-[jekfr][ranou]\|([^}{|]+)\|([^}{|]+)\}\}', r'\1', text)#{{lang-ja|'''まどひ白きの神隠し'''|ja}}

    text = re.sub(r'\{\{[Ll]ang-[jekfr][ranou]\|([^}{]+)\}\}', r'\1', text)#匹配[Ll]ang-[jekfr]

    text = re.sub(r'\{\{[Ll]ang\|[jekfr][ranou]\|((?:[^}{]|\n)+)\}\}', r'\1', text)#匹配[Ll]ang|[jekfr][ranou]|
    print(f"{input_file_name}转换进度15/40")
    text = re.sub(r"\{\{jpn\|([^|}{]+)\|([^|}{]+)\|([^|}{]+)\|([^|}{]*)[^}{]*\}\}", r'\1\3', text)#匹配{{jpn|千歳|ちとせ|春樹|はるき|nobr=true}}

    text = re.sub(r"\{\{[Rr]ubya|([^_}{]+)_([^|}{]+)|([^_}{]+)_([^}{]*)\}\}", r'\1 \3', text)#匹配{{rubya|天道_てんどう|マリア_}} ————>天道 マリア

    text = re.sub(r"\{\{[Rr]ubyh\|([^|}{]+)\|([^}{]+)\}\}", r'\1', text)#匹配{{Rubyh|奇怪|糟糕}} ————>奇怪

    text = re.sub(r'\{\{黑幕\|([^}{|]+)(\|)*[^}{|]+\}\}', r'\1', text)#黑幕

    text = re.sub(r'\{\{交叉颜色\|c1=#[0-9a-fA-F]{1,9}\|c2=#[0-9a-fA-F]{1,9}\|([^|}{]+)\|([^|}{]+)\|([^|}{]+)\}\}', r'\1\2\3', text)
    print(f"{input_file_name}转换进度20/40")
    text = re.sub(r'\{\{交叉颜色\|c1=#[0-9a-fA-F]{1,9}\|c2=#[0-9a-fA-F]{1,9}\|([^|}{]+)\|([^|}{]+)\|([^|}{]+)\|([^|}{]+)\|([^|}{]+)\}\}', r'\1\2\3\4\5', text)

    text = re.sub(r'\{\{交叉颜色F\|#[0-9a-fA-F]{1,9},#[0-9a-fA-F]{1,9},#[0-9a-fA-F]{1,9}\|([^|}{]+)\}\}', r'\1', text)
    #第二轮2
    text = re.sub(r"（\[https?://[^\}{]+\]）", r'', text)

    text = re.sub(r"（\{\{ISBN\|[^}{]+\}\}）", r'', text)

    text = re.sub(r'\{\{dead\|([^}]+)\}\}', r'\1', text)#匹配dead
    print(f"{input_file_name}转换进度25/40")
    text = re.sub(r'\[\[(?!File:)(?!文件:)(?![Ii]mage:)(?!#)[^[}{\]|]*\|(?!\*)([^}{[\]]*)\]\]', r'\1', text)#匹配[[实际页面|显示文字]]]

    text = re.sub(r'\{\{[Rr]uby\|([^|}{]+)\|([^|}{]+)[|jaenzh]*\}\}', r'\1', text) #匹配[Rr]uby

    text = re.sub(r'\[\[(?!File:)(?!文件:)(?![Ii]mage:)(?!#)[^[}{\]|]*\|(?!\*)([^}{[\]]*)\]\]', r'\1', text)#匹配[[实际页面|显示文字]]] for {{lang|ja|「[[致永远之星|{{ruby|永遠|とわ}}の星へ]]」}}

    text = re.sub(r'\{\{[Ff]ont[^}{]*\|((?:[^}{]|\n)+)\}\}', r'\1', text)#匹配[Ff]ont

    text = re.sub(r'\{\{[Ll]j\|((?:[^}{]|\n)+)\}\}', r'\1', text)#匹配[Ll]j
    print(f"{input_file_name}转换进度30/40")
    text = re.sub(r'\{\{[Cc]olor\|[^|}{]+\|((?:[^}{]+)|\n)\}\}', r'\1', text)#匹配color

    text = re.sub(r'\{\{coloredlink\|[^|}{]+\|([^}{]+)\}\}', r'\1', text)#匹配coloredlink

    text = re.sub(r'\{\{[Ll]ang-[jekfr][ranou]\|([^}{|]+)\|([^}{|]+)\}\}', r'\1', text)#{{lang-ja|'''まどひ白きの神隠し'''|ja}}

    text = re.sub(r'\{\{[Ll]ang-[jekfr][ranou]\|([^}{]+)\}\}', r'\1', text)#匹配[Ll]ang-[jekfr]

    text = re.sub(r'\{\{[Ll]ang\|[jekfr][ranou]\|((?:[^}{]|\n)+)\}\}', r'\1', text)#匹配[Ll]ang|[jekfr][ranou]|
    print(f"{input_file_name}转换进度35/40")
    text = re.sub(r"\{\{jpn\|([^|}{]+)\|([^|}{]+)\|([^|}{]+)\|([^|}{]*)[^}{]*\}\}", r'\1\3', text)#匹配{{jpn|千歳|ちとせ|春樹|はるき|nobr=true}}

    text = re.sub(r"\{\{[Rr]ubya|([^_}{]+)_([^|}{]+)|([^_}{]+)_([^}{]*)\}\}", r'\1 \3', text)#匹配{{rubya|天道_てんどう|マリア_}} ————>天道 マリア

    text = re.sub(r"\{\{[Rr]ubyh\|([^|}{]+)\|([^}{]+)\}\}", r'\1', text)#匹配{{Rubyh|奇怪|糟糕}} ————>奇怪

    text = re.sub(r"\{\{背景[图圖]片(?!区域)(?:[^}{]|\n)*\}\}", r'', text)#匹配并删除背景[图圖]片
    print(f"{input_file_name}转换进度39/40")
    text = re.sub(r"\{\{背景[图圖]片区域(?:[^}{]|\n)*\|([^}{|]*)\}\}", r'\1', text)#匹配背景[图圖]片区域提取文字

    return text

def convert_to_plain_text(mediawiki_text):
    wikicode = mwparser.parse(mediawiki_text)
    plain_text = wikicode.strip_code()
    return plain_text

def main(input_path, output_path):
    base_file_name = os.path.splitext(os.path.basename(input_path))[0]
    # 读取输入文件内容
    with open(input_path, 'r', encoding='utf-8') as input_file:
        mediawiki_text = input_file.read()
        preprocessed_text = preprocess_text(mediawiki_text, base_file_name)
        #plain_text = convert_to_plain_text(preprocessed_text)
        plain_text = preprocessed_text

    #plain_text = plain_text.lstrip('}}\n\n ')

    # 创建数据字典并写入输出文件
    data = [{"text": plain_text, "source": "moegril"}]
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)

    print(f"{base_file_name}转换完成")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert_mediawiki_to_json.py input_file output_file")
    else:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        main(input_file_path, output_file_path)
