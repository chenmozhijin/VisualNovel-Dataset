#!/bin/bash

# 设置要处理的文件和输出文件
input_file="wikipedia_page_id.txt"
output_file="zhwiki-vn.xml"
max_parallel_processes=8  # 设置最大并行进程数量

# 删除旧的输出文件（如果需要）
rm -f "$output_file"

# 获取总共要处理的 ID 数量
total_ids=$(wc -l < "$input_file")
echo "Total pages to process: $total_ids"

# 记录脚本开始时间
start_time=$(date +%s)

# 显示进度函数
show_progress() {
    percentage=$((processed_ids * 100 / total_ids))
    echo -ne "Progress: $processed_ids/$total_ids ($percentage%) \r"
}

# 逐行读取输入文件
while IFS= read -r id; do
    (
        # 在子shell中执行命令并将输出追加到输出文件
        extractPage --id "$id" zhwiki.xml >> "$output_file"
    ) &  # 将子shell放入后台执行

    # 控制并行进程数量
    running_processes=$(jobs -p | wc -l)
    if (( running_processes >= max_parallel_processes )); then
        wait -n  # 等待任一后台进程完成
        processed_ids=$((processed_ids + 1))  # 在等待之后增加已处理的 ID 数量
        show_progress
    fi
done < "$input_file"

# 等待所有后台进程完成
wait

# 计算脚本运行耗时
end_time=$(date +%s)
elapsed_time=$((end_time - start_time))
echo "Total time elapsed: $elapsed_time seconds"

# 最后输出一个换行，以使进度信息不与提示符混合
echo ""

# 完成后的其他处理可以在这里添加
