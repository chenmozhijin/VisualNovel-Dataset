#!/usr/bin/env bash
rows=1
total_rows=$(sed -n '$=' wikipedia_page_id.txt)
echo '总id数：' $total_rows
until [ "$rows" -gt $total_rows ]; do
    id=$(sed -n "${rows}p" wikipedia_page_id.txt)
    extractPage --id $id zhwiki.xml >> zhwiki-vn.xml
    echo '已完成' $rows '/' $total_rows
    rows=$(($rows+1))
done