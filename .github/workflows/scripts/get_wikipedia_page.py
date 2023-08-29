import os
import subprocess
import re
from multiprocessing import Pool, Value

# 获取运行目录下的所有符合文件名格式的文件
def get_matching_files():
    matching_files = []
    pattern = r'zhwiki-latest-pages-articles-multistream\d+\.xml-p\d+p\d+$'
    for filename in os.listdir():
        if re.match(pattern, filename):
            matching_files.append(filename)
    return matching_files

# 读取页面ID文件
def read_page_ids(filename):
    with open(filename, 'r') as file:
        page_ids = [line.strip() for line in file]
    return page_ids

# 执行extractPage命令
def extract_page(args):
    file, page_id = args
    command = f"extractPage --id {page_id} {file} >> zhwiki-vn.xml"
    subprocess.run(command, shell=True)
    with processed_ids.get_lock():
        processed_ids.value += 1
        processed_percent = (processed_ids.value / total_valid_ids) * 100
        print(f"进度：{processed_ids.value}/{total_valid_ids} ({processed_percent:.2f}%) - 处理页面ID {page_id}")

if __name__ == "__main__":
    # 步骤1：获取运行目录下的文件名为"zhwiki-latest-pages-articles-multistream$(文件id).xml-p$(开始页id)p$(结束页id)"格式的文件
    matching_files = get_matching_files()

    if not matching_files:
        print("没有符合要求的文件")
        exit()
    else:
        print("处理以下文件：")
        print(*matching_files, sep = "\n")

    # 步骤2：读取页面ID文件
    page_id_file = "wikipedia_page_id.txt"
    page_ids = read_page_ids(page_id_file)

    if not page_ids:
        print("页面ID文件为空")
        exit()

    # 步骤3：计算未跳过的ID总数和已跳过的ID数
    total_valid_ids = 0
    skipped_ids = 0
    for page_id in page_ids:
        found_matching_file = False
        for file in matching_files:
            start_id, end_id = re.findall(r'(\d+)', file)[-2:]
            if int(start_id) <= int(page_id) <= int(end_id):
                total_valid_ids += 1
                found_matching_file = True
                break

        if not found_matching_file:
            skipped_ids += 1
            print(f"页面ID {page_id} 没有匹配的文件，已跳过")

    processed_ids = Value('i', 0)  # 用于记录已处理的未跳过的ID个数，带锁

    # 步骤4：删除已存在的zhwiki-vn.xml文件
    if os.path.exists("zhwiki-vn.xml"):
        print("删除已存在的zhwiki-vn.xml文件")
        os.remove("zhwiki-vn.xml")

    # 步骤5：对每个页面ID进行处理，使用多线程同时执行
    pool = Pool(processes=4)  # 4个并发线程，可以根据需要调整

    print("开始处理")

    for page_id in page_ids:
        found_matching_file = False
        for file in matching_files:
            start_id, end_id = re.findall(r'(\d+)', file)[-2:]
            if int(start_id) <= int(page_id) <= int(end_id):
                pool.apply_async(extract_page, ((file, page_id),))
                found_matching_file = True
                break

    pool.close()
    pool.join()

    print(f"处理完成，已跳过ID数：{skipped_ids}/{len(page_ids)}")

    # 步骤6：从选定文件中选择第一行和最后一行插入到zhwiki-vn.xml中
    selected_file = matching_files[0]  # 从第一个文件中选择
    with open(selected_file, "r") as selected_file_content:
        selected_first_line = selected_file_content.readline()
        selected_last_line = selected_file_content.readlines()[-1]

    with open("zhwiki-vn.xml", "r") as current_file:
        current_content = current_file.read()

    with open("zhwiki-vn.xml", "w") as output_file:
        output_file.write(selected_first_line + current_content + selected_last_line)

    print(f"已插入文件 {selected_file} 的第一行和最后一行到 zhwiki-vn.xml")
