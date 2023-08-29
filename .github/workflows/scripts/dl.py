import requests
import re
import subprocess

# 请求网页内容
url = 'https://dumps.wikimedia.org/zhwiki/latest/'
response = requests.get(url)
webpage_content = response.text

# 正则表达式模式，匹配指定文件名格式的链接
pattern = r'zhwiki-latest-pages-articles-multistream(\d+)\.xml-p(\d+)p(\d+)\.bz2'
download_links = re.findall(pattern, webpage_content)

# 构建完整的下载链接并去重
base_download_url = 'https://dumps.wikimedia.org/zhwiki/latest/'
download_urls = set([
    f"{base_download_url}zhwiki-latest-pages-articles-multistream{file_id}.xml-p{start_page_id}p{end_page_id}.bz2"
    for file_id, start_page_id, end_page_id in download_links
])

# 对下载链接进行排序
sorted_download_urls = sorted(download_urls)

# 设置aria2下载参数
aria2_args = [
    'aria2c',
    '-x', '16',  # 16线程下载
    '-j', '5',   # 最大同时下载任务数
    '--retry-wait', '5',  # 下载失败后重试等待时间
]

# 下载每个链接
for download_url in sorted_download_urls:
    aria2_args.append(download_url)

    try:
        # 调用aria2命令行下载工具
        subprocess.run(aria2_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"下载失败: {e}")
    
    # 移除当前链接，以便添加下一个链接
    aria2_args.pop()

print("下载完成")
