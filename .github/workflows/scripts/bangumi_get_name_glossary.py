# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright (c) 2024 沉默の金
import os
import json
import re
import requests
import logging
import zipfile
from tqdm import tqdm

def get_newest_archive():
    url = "https://api.github.com/repos/bangumi/Archive/releases/tags/archive"
    response = requests.get(url)
    release = response.json()

    newest_asset = max(release["assets"], key=lambda asset: asset["created_at"])

    asset_download_url = newest_asset["browser_download_url"]
    return asset_download_url

def download_file(url: str, file_dir: str, file_name: str | None = None) -> str:
    """
    文件下载
    :param url: 下载链接
    :param file_dir: 保存路径(文件夹)
    :param file_name: 文件名
    :return: 文件路径
    """
    logging.info(f"文件下载: {url}")
    response = requests.get(url, allow_redirects=True, stream=True)  # noqa: S113
    response.raise_for_status()
    file_size = int(response.headers.get("content-length", 0))
    if not isinstance(file_name, str):
        file_name = response.url.split("/")[-1]
    file_path = os.path.join(file_dir, file_name)
    if os.path.exists(file_path):
        logging.info(f"{file_name}已存在，删除")
        os.remove(file_path)
    with open(file_path, "wb") as f:
        # 同时回传进度信号
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                logging.info(f"正在下载{file_name}, {f.tell() / file_size * 100:.2f}%")
    return file_path

def get_archive():
    logging.info("获取最新归档")
    url = get_newest_archive()
    file_path = download_file(url, "/tmp", "archive")

    zipfile.ZipFile(file_path).extractall("/tmp")

get_archive()

def clear(content):
    content = content.replace("\t", "")
    content = content.replace("\n", "")
    content = content.replace("\r", "")
    content = content.replace("‎", "")
    content = re.sub(r"^ +| +$", "", content)
    content = re.sub(r"[（(\[【［][^)）】\]］]*[】］\])）]", "", content)
    return content


results = []

def clear(content):
    content = content.replace("\t", "")
    content = content.replace("\n", "")
    content = content.replace("\r", "")
    content = content.replace("‎", "")
    content = re.sub(r"^ +| +$", "", content)
    content = re.sub(r"[（(\[【［][^)）】\]］]*[】］\])）]", "", content)
    return content


results = []

logging.info("开始加载character.jsonlines")
with open("/tmp/character.jsonlines", 'r', encoding='utf-8') as file:
    contents = [json.loads(line) for line in file]
logging.info("开始加载subject-characters.jsonlines")
with open("/tmp/subject-characters.jsonlines", 'r', encoding='utf-8') as file:
    subject_characters = [json.loads(line) for line in file]
logging.info("开始加载subject.jsonlines")
with open("/tmp/subject.jsonlines", 'r', encoding='utf-8') as file:
    o_subjects = [json.loads(line) for line in file]

logging.info("开始处理subjects")
o_subjects_dict = {item["id"]: item for item in o_subjects}
o_subjects = None
mapping = {}

logging.info("开始处理subject-characters映射表")
total = len(subject_characters)
for subject_character in tqdm(subject_characters, total=total):
    character_id = subject_character['character_id']
    subject_id = subject_character['subject_id']

    subject = o_subjects_dict.get(subject_id)

    if subject is None:
        continue
    subject_name = subject['name']
    subject_name_zh = subject['name_cn']
    subject_type: int = subject['type']
    if character_id not in mapping:
        mapping[character_id] = []
    mapping[character_id].append({"subject_id": subject_id, "subject_name": subject_name, "subject_name_zh": subject_name_zh, "subject_type": subject_type})


logging.info("开始生成结果")
# 遍历contents列表中的每一项
total = len(contents)
for content in tqdm(contents, total=total):
    # 获取infobox内容
    infobox = content["infobox"]
    if content["id"] == 28556:
        pass
    # 如果infobox中包含[日文名|]或者infobox中不包含简体中文名和[日文名|]
    if "[日文名|]" in infobox or not ("简体中文名= " in infobox and ("[日文名|" in infobox or ("[第二日文名|" in infobox and "[第二日文名|]" not in infobox))):
        # 跳过本次循环
        continue
    info = {}
    # 使用正则表达式从infobox中获取简体中文名
    info["zh_name"] = re.findall(r"简体中文名= ([^\r\n]*)\r?\n.*", infobox)
    info["zh_name2"] = re.findall(r"\[第二中文名\|([^\]]+)\]", infobox)
    # 使用正则表达式从infobox中获取日文名
    info["ja_name"] = re.findall(r"\[日文名\|([^\]]+)\]", infobox)
    info["ja_name2"] = re.findall(r"\[第二日文名\|([^\]]+)\]", infobox)
    # 使用正则表达式从infobox中获取假名
    info["kana_name"] = re.findall(r"\[纯假名\|([^\]]+)\]", infobox)
    info["kana_name2"] = re.findall(r"\[第二纯假名\|([^\]]+)\]", infobox)
    # 使用正则表达式从infobox中获取英文名
    info["en_name"] = re.findall(r"\[英文名\|([^\]]+)\]", infobox)
    info["en_name2"] = re.findall(r"\[第二英文名\|([^\]]+)\]", infobox)
    info["gender"] = re.findall(r"\|性别= ([^\r\n]*)\r?\n\|", infobox)
    info["nick_name"] = re.findall(r"\[昵称\|([^\]]+)\]", infobox)
    info["nick_name2"] = re.findall(r"\[第二昵称\|([^\]]+)\]", infobox)
    # 如果简体中文名或者日文名不存在，则跳过本次循环
    for key, item in info.items():
        if key == "gender" and item:
            pass
        if not item or item[0] == "":
            if key not in ["gender"]:
                info[key] = []
            else:
                info[key] = ""
            continue
        cleared_item = clear(item[0])
        if "／" in cleared_item:
            cleared_item = re.sub(r"\s*[／/]\s*", "/", cleared_item)
        if "/" in cleared_item:
            cleared_item = cleared_item.split("/")
        elif key not in ["gender"]:
            cleared_item = [cleared_item]
        info[key] = cleared_item

    zh_name: list = info["zh_name"]
    zh_name2: list = info["zh_name2"]
    ja_name: list = info["ja_name"]
    ja_name2: list = info["ja_name2"]
    kana_name: list = info["kana_name"]
    kana_name2: list = info["kana_name2"]
    en_name: list = info["en_name"]
    en_name2: list = info["en_name2"]
    gender: str = info["gender"]
    nick_name: list = info["nick_name"]
    nick_name2: list = info["nick_name2"]

    subjects = mapping.get(content["id"], [])

    if zh_name2:
        zh_name.extend(zh_name2)
    if ja_name2:
        ja_name.extend(ja_name2)
    if kana_name2:
        kana_name.extend(kana_name2)
    if en_name2:
        en_name.extend(en_name2)
    if nick_name2:
        nick_name.extend(nick_name2)

    if not zh_name or not ja_name:
        continue
    else:
        result = {"id": content["id"], "zh": zh_name, "ja": ja_name, "en": en_name, "kana": kana_name, "nick_name": nick_name, "gender": gender, "subjects": subjects}
        results.append(result)

with open("character.jsonl", 'w', encoding='utf-8') as file:
    for item in results:
        file.write(json.dumps(item, ensure_ascii=False) + "\n")
