import requests
import re
import threading
import pywget

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

# 定义下载函数
def download_file(url):
    try:
        pywget.download(url)
        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Failed to download: {url}")
        print(f"Error: {e}")
        print("Retrying...")
        download_file(url)  # 递归进行重试

# 设置并发线程数
max_threads = 4

# 多线程下载
threads = []
for download_url in sorted_download_urls:
    # 控制并发线程数
    while len(threads) >= max_threads:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
                break

    thread = threading.Thread(target=download_file, args=(download_url,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print("All downloads completed.")
