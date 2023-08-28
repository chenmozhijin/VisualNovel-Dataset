import requests

# 设置API的URL和公共参数
base_url = "https://zh.wikipedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "list": "categorymembers",
    "cmlimit": 500,  # 每页返回的数量
}

# 指定多个分类名称
categories = ["Category:視覺小說", "Category:美少女遊戲"]  # 替换成你想要的分类名称

# 存储所有页面ID的集合
all_page_ids = set()

# 遍历每个分类，获取页面ID
for category in categories:
    continue_flag = True
    cmcontinue = None
    
    while continue_flag:
        params["cmtitle"] = category
        if cmcontinue:
            params["cmcontinue"] = cmcontinue
        
        # 发送API请求
        response = requests.get(base_url, params=params)
        data = response.json()

        # 处理API响应，提取页面ID
        page_ids = [page["pageid"] for page in data["query"]["categorymembers"]]
        
        # 将页面ID添加到集合中
        all_page_ids.update(page_ids)
        
        # 检查是否有更多页面需要获取
        if "continue" in data:
            cmcontinue = data["continue"]["cmcontinue"]
        else:
            continue_flag = False

# 将合并后的页面ID写入文件
with open("wikipedia_page_id.txt", "w") as file:
    for page_id in all_page_ids:
        file.write(str(page_id) + "\n")

print("页面ID已保存到文件：wikipedia_page_id.txt")