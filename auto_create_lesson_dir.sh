#!/bin/bash

lesson=$1

# 创建 day$1 为名的目录
mkdir day${lesson}

# 生成 README.md
cd day${lesson}
touch README.md

# 写入特定内容
echo "## 上课时间\n\n\n## 作业\n" > README.md