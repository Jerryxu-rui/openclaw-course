#!/bin/bash

# 橙皮书内容分割脚本
# 将橙皮书文本按Part分割为单独的文件

cd "$(dirname "$0")"

INPUT_FILE="orange-book-text.txt"
OUTPUT_DIR="orange-book-parts"

# 获取每个Part的起始行号
echo "分析橙皮书结构..."
PART_LINES=$(grep -n "Part " "$INPUT_FILE")

# 提取行号数组
declare -a START_LINES
while IFS= read -r line; do
    line_num=$(echo "$line" | cut -d: -f1)
    START_LINES+=("$line_num")
done <<< "$PART_LINES"

# 添加文件结束行号
FILE_END=$(wc -l < "$INPUT_FILE")
START_LINES+=("$((FILE_END + 1))")

echo "找到 ${#START_LINES[@]} 个Part（包括文件结束）"

# 分割每个Part
for ((i=0; i<${#START_LINES[@]}-1; i++)); do
    start_line=${START_LINES[i]}
    end_line=$(( ${START_LINES[i+1]} - 1 ))
    
    # 获取Part标题
    part_title=$(sed -n "${start_line}p" "$INPUT_FILE")
    part_num=$((i+1))
    
    echo "处理 Part $part_num: $part_title (行 $start_line-$end_line)"
    
    # 提取内容
    sed -n "${start_line},${end_line}p" "$INPUT_FILE" > "$OUTPUT_DIR/part${part_num}.txt"
    
    # 统计行数
    line_count=$(wc -l < "$OUTPUT_DIR/part${part_num}.txt")
    echo "  保存到 part${part_num}.txt ($line_count 行)"
done

echo "分割完成！"
echo "输出目录: $OUTPUT_DIR/"
ls -la "$OUTPUT_DIR/"