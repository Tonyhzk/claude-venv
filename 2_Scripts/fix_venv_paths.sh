#!/bin/bash
# ==================== 修复 .venv 中的绝对路径 ====================
# 此脚本将虚拟环境中的硬编码绝对路径替换为相对路径或动态路径

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "============================================================"
echo "🔧 修复虚拟环境中的绝对路径"
echo "============================================================"
echo "📍 项目路径: $SCRIPT_DIR"
echo "📦 虚拟环境: $VENV_DIR"
echo ""

# 检查虚拟环境是否存在
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ 错误：虚拟环境不存在"
    exit 1
fi

# 备份计数
BACKUP_COUNT=0

# ==================== 1. 修复 activate 脚本 (Bash/Zsh) ====================
echo "📝 [1/5] 修复 activate 脚本..."

ACTIVATE_FILE="$VENV_DIR/bin/activate"
if [ -f "$ACTIVATE_FILE" ]; then
    # 备份原文件
    cp "$ACTIVATE_FILE" "$ACTIVATE_FILE.backup"
    BACKUP_COUNT=$((BACKUP_COUNT + 1))
    
    # 替换绝对路径为动态检测
    sed -i '' 's|^VIRTUAL_ENV=".*\.venv"$|VIRTUAL_ENV="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." \&\& pwd)"|' "$ACTIVATE_FILE"
    
    echo "   ✅ activate 已修复"
else
    echo "   ⚠️  activate 文件不存在"
fi

# ==================== 2. 修复 activate.fish 脚本 ====================
echo "📝 [2/5] 修复 activate.fish 脚本..."

ACTIVATE_FISH="$VENV_DIR/bin/activate.fish"
if [ -f "$ACTIVATE_FISH" ]; then
    cp "$ACTIVATE_FISH" "$ACTIVATE_FISH.backup"
    BACKUP_COUNT=$((BACKUP_COUNT + 1))
    
    # Fish shell 使用不同的语法
    sed -i '' 's|^set -gx VIRTUAL_ENV ".*\.venv"$|set -gx VIRTUAL_ENV (cd (dirname (status -f))/..; and pwd)|' "$ACTIVATE_FISH"
    
    echo "   ✅ activate.fish 已修复"
else
    echo "   ⚠️  activate.fish 文件不存在"
fi

# ==================== 3. 修复 activate.csh 脚本 ====================
echo "📝 [3/5] 修复 activate.csh 脚本..."

ACTIVATE_CSH="$VENV_DIR/bin/activate.csh"
if [ -f "$ACTIVATE_CSH" ]; then
    cp "$ACTIVATE_CSH" "$ACTIVATE_CSH.backup"
    BACKUP_COUNT=$((BACKUP_COUNT + 1))
    
    # C shell 语法
    sed -i '' 's|^setenv VIRTUAL_ENV ".*\.venv"$|setenv VIRTUAL_ENV `cd \`dirname $0\`/..; pwd`|' "$ACTIVATE_CSH"
    
    echo "   ✅ activate.csh 已修复"
else
    echo "   ⚠️  activate.csh 文件不存在"
fi

# ==================== 4. 修复 Activate.ps1 脚本 (PowerShell) ====================
echo "📝 [4/5] 修复 Activate.ps1 脚本..."

ACTIVATE_PS1="$VENV_DIR/bin/Activate.ps1"
if [ -f "$ACTIVATE_PS1" ]; then
    cp "$ACTIVATE_PS1" "$ACTIVATE_PS1.backup"
    BACKUP_COUNT=$((BACKUP_COUNT + 1))
    
    # PowerShell 语法
    sed -i '' 's|^\$env:VIRTUAL_ENV=".*\.venv"$|$env:VIRTUAL_ENV=(Get-Item (Split-Path -Parent $PSCommandPath)).Parent.FullName|' "$ACTIVATE_PS1"
    
    echo "   ✅ Activate.ps1 已修复"
else
    echo "   ⚠️  Activate.ps1 文件不存在"
fi

# ==================== 5. 修复可执行文件的 shebang ====================
echo "📝 [5/5] 修复可执行文件的 shebang..."

# 查找所有包含绝对路径 shebang 的 Python 脚本
FIXED_COUNT=0
for file in "$VENV_DIR/bin"/*; do
    if [ -f "$file" ] && [ -x "$file" ]; then
        # 检查是否是 Python 脚本且包含绝对路径
        if head -1 "$file" 2>/dev/null | grep -q "^#!.*\.venv/bin/python"; then
            # 备份
            cp "$file" "$file.backup"
            BACKUP_COUNT=$((BACKUP_COUNT + 1))
            
            # 替换 shebang 为 /usr/bin/env python
            sed -i '' '1s|^#!/.*\.venv/bin/python.*$|#!/usr/bin/env python|' "$file"
            
            FIXED_COUNT=$((FIXED_COUNT + 1))
        fi
    fi
done

echo "   ✅ 已修复 $FIXED_COUNT 个可执行文件的 shebang"

# ==================== 完成 ====================
echo ""
echo "============================================================"
echo "✅ 修复完成！"
echo "============================================================"
echo "📊 统计信息："
echo "   - 备份文件数: $BACKUP_COUNT"
echo "   - 修复的 shebang: $FIXED_COUNT"
echo ""
echo "💡 提示："
echo "   1. 原文件已备份为 *.backup"
echo "   2. 现在可以安全地移动整个项目目录"
echo "   3. 使用 run.sh/run.py/run.bat 启动，它们会动态设置路径"
echo ""
echo "🧪 验证修复："
echo "   ./run.sh --version"
echo ""
