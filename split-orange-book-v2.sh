#!/bin/bash

# 橙皮书内容分割脚本 v2
# 更精确地分割橙皮书内容

cd "$(dirname "$0")"

INPUT_FILE="orange-book-text.txt"
OUTPUT_DIR="orange-book-parts-v2"

mkdir -p "$OUTPUT_DIR"

# 定义分割点（行号）
PART1_START=26   # Part 1: 认识 OpenClaw
PART2_START=43   # Part 2: 技术架构
PART3_START=64   # Part 3: 部署方案
PART4_START=85   # Part 4: 渠道接入
PART5_START=102  # Part 5: Skills 系统
PART6_START=123  # Part 6: 模型配置
PART7_START=140  # Part 7: 安全与成本
PART8_START=153  # Part 8: 生态与社区
APPENDIX_START=170 # 附录开始
FILE_END=5644    # 文件结束

echo "开始分割橙皮书内容..."

# Part 1: 认识 OpenClaw
echo "提取 Part 1 (行 $PART1_START-$((PART2_START-1)))"
sed -n "${PART1_START},$((PART2_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part1-认识-OpenClaw.txt"

# Part 2: 技术架构
echo "提取 Part 2 (行 $PART2_START-$((PART3_START-1)))"
sed -n "${PART2_START},$((PART3_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part2-技术架构.txt"

# Part 3: 部署方案
echo "提取 Part 3 (行 $PART3_START-$((PART4_START-1)))"
sed -n "${PART3_START},$((PART4_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part3-部署方案.txt"

# Part 4: 渠道接入
echo "提取 Part 4 (行 $PART4_START-$((PART5_START-1)))"
sed -n "${PART4_START},$((PART5_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part4-渠道接入.txt"

# Part 5: Skills 系统
echo "提取 Part 5 (行 $PART5_START-$((PART6_START-1)))"
sed -n "${PART5_START},$((PART6_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part5-Skills系统.txt"

# Part 6: 模型配置
echo "提取 Part 6 (行 $PART6_START-$((PART7_START-1)))"
sed -n "${PART6_START},$((PART7_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part6-模型配置.txt"

# Part 7: 安全与成本
echo "提取 Part 7 (行 $PART7_START-$((PART8_START-1)))"
sed -n "${PART7_START},$((PART8_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part7-安全与成本.txt"

# Part 8: 生态与社区（不含附录）
echo "提取 Part 8 (行 $PART8_START-$((APPENDIX_START-1)))"
sed -n "${PART8_START},$((APPENDIX_START-1))p" "$INPUT_FILE" > "$OUTPUT_DIR/part8-生态与社区.txt"

# 附录
echo "提取 附录 (行 $APPENDIX_START-$FILE_END)"
sed -n "${APPENDIX_START},${FILE_END}p" "$INPUT_FILE" > "$OUTPUT_DIR/appendix-附录.txt"

echo "分割完成！"
echo "输出目录: $OUTPUT_DIR/"
ls -la "$OUTPUT_DIR/" | while read line; do
    filename=$(echo "$line" | awk '{print $9}')
    if [ -n "$filename" ]; then
        lines=$(wc -l < "$OUTPUT_DIR/$filename" 2>/dev/null || echo "0")
        size=$(echo "$line" | awk '{print $5}')
        echo "  $filename: $lines 行, $size 字节"
    fi
done