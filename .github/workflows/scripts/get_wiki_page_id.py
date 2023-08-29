import requests
import argparse

# 定义不同百科的api地址与指定分类
wikis = {
    'zh-wikipedia': {
        'api_url': 'https://zh.wikipedia.org/w/api.php',
        'categories': ['視覺小說', '美少女遊戲']  # 示例分类名，根据实际需求修改
    },
    'moegirl': {
        'api_url': 'https://zh.moegirl.org.cn/api.php',
        'categories': ['恋爱冒险游戏', '视觉小说']  # 示例分类名，根据实际需求修改
    }
}

def get_page_ids(api_url, category):
    # 设置请求参数
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category}',
        'cmlimit': 500
    }

    page_ids = []

    # 循环请求，直到获取全部页面
    while True:
        response = requests.get(api_url, params=params)
        data = response.json()

        for item in data['query']['categorymembers']:
            page_ids.append(item['pageid'])

        if 'continue' in data:
            params['cmcontinue'] = data['continue']['cmcontinue']
        else:
            break

    return page_ids

def main():
    parser = argparse.ArgumentParser(description='获取多个百科指定分类下的页面ID')
    parser.add_argument('wiki', choices=wikis.keys(), help='要获取页面ID的百科')
    args = parser.parse_args()

    wiki_info = wikis[args.wiki]
    api_url = wiki_info['api_url']
    categories = wiki_info['categories']

    all_page_ids = []

    for category in categories:
        page_ids = get_page_ids(api_url, category)
        all_page_ids.extend(page_ids)

    # 去重并排序
    all_page_ids = sorted(list(set(all_page_ids)))

    # 存储页面ID到文件
    filename = f'{args.wiki}-page_ids.txt'
    with open(filename, 'w') as file:
        for page_id in all_page_ids:
            file.write(f'{page_id}\n')

    print(f'已存储{args.wiki}页面ID数量：{len(all_page_ids)}')

if __name__ == '__main__':
    main()
