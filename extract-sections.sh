#!/bin/bash

# 提取橙皮书章节内容脚本

cd "$(dirname "$0")"

INPUT_FILE="appendix-complete.txt"
OUTPUT_DIR="orange-book-sections"

mkdir -p "$OUTPUT_DIR"

echo "开始提取橙皮书章节内容..."

# 获取所有章节行号
echo "查找章节行号..."
SECTION_LINES=$(grep -n "^[0-9][0-9]$" "$INPUT_FILE")

# 提取行号数组
declare -a LINE_NUMS
declare -a SECTION_IDS
while IFS= read -r line; do
    line_num=$(echo "$line" | cut -d: -f1)
    section_id=$(echo "$line" | cut -d: -f2)
    LINE_NUMS+=("$line_num")
    SECTION_IDS+=("$section_id")
done <<< "$SECTION_LINES"

# 添加文件结束行号
FILE_END=$(wc -l < "$INPUT_FILE")
LINE_NUMS+=("$((FILE_END + 1))")

echo "找到 ${#SECTION_IDS[@]} 个章节"

# 提取每个章节
for ((i=0; i<${#SECTION_IDS[@]}; i++)); do
    section_id=${SECTION_IDS[i]}
    start_line=${LINE_NUMS[i]}
    end_line=$(( ${LINE_NUMS[i+1]} - 1 ))
    
    echo "提取章节 $section_id (行 $start_line-$end_line)"
    
    # 提取内容
    sed -n "${start_line},${end_line}p" "$INPUT_FILE" > "$OUTPUT_DIR/section-${section_id}.txt"
    
    # 统计行数
    line_count=$(wc -l < "$OUTPUT_DIR/section-${section_id}.txt")
    echo "  保存到 section-${section_id}.txt ($line_count 行)"
done

echo "提取完成！"
echo "输出目录: $OUTPUT_DIR/"
ls -la "$OUTPUT_DIR/" | head -20