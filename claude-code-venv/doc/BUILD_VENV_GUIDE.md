# Claude Code 虚拟环境构建指南

> 使用 `build_venv.py` 脚本快速构建跨平台虚拟环境

## 📋 目录

- [功能概述](#功能概述)
- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [使用方法](#使用方法)
- [构建流程](#构建流程)
- [常见问题](#常见问题)
- [高级用法](#高级用法)

## 功能概述

`build_venv.py` 是一个自动化脚本，用于构建 Claude Code 的完整虚拟环境。它可以：

- ✅ 自动检测当前操作系统
- ✅ 创建 Python 虚拟环境（venv_mac、venv_linux、venv_win）
- ✅ 安装 nodeenv 并嵌入 Node.js 环境
- ✅ 通过 npm 安装 Claude Code
- ✅ 创建便捷的激活脚本（activate_claude）
- ✅ 验证安装是否成功
- ✅ 支持选择性构建或批量构建
- ✅ 支持自定义 Node.js 版本
- ✅ 提供详细的构建日志和错误提示

## 系统要求

### 基本要求

- **Python**: 3.8 或更高版本
- **网络**: 需要访问 PyPI 下载包
- **磁盘空间**: 每个虚拟环境约 200-300 MB

### 平台特定要求

#### macOS
- Python 3.8+（通常系统自带或通过 Homebrew 安装）
- 命令行工具（Xcode Command Line Tools）

#### Linux
- Python 3.8+
- python3-venv 包（某些发行版需要单独安装）
  ```bash
  # Ubuntu/Debian
  sudo apt-get install python3-venv
  
  # CentOS/RHEL
  sudo yum install python3-venv
  ```

#### Windows
- Python 3.8+（从 python.org 下载安装）
- 确保 Python 已添加到 PATH

## 快速开始

### 1. 进入项目目录

```bash
cd /path/to/claude-code-venv
```

### 2. 运行构建脚本

```bash
# 构建当前系统的虚拟环境
python3 build_venv.py

# 或者查看帮助
python3 build_venv.py --help
```

### 3. 等待构建完成

脚本会自动完成以下步骤：
1. 检查 Python 版本
2. 创建虚拟环境
3. 安装 Claude Code
4. 验证安装

### 4. 配置并启动

```bash
# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 API 密钥

# 启动 Claude Code
python3 run.py
```

## 使用方法

### 基本命令

```bash
# 构建当前系统的虚拟环境（自动检测）
python3 build_venv.py

# 构建所有平台的虚拟环境
python3 build_venv.py --all

# 只构建 macOS 虚拟环境
python3 build_venv.py --mac

# 只构建 Linux 虚拟环境
python3 build_venv.py --linux

# 只构建 Windows 虚拟环境
python3 build_venv.py --win

# 构建多个指定平台
python3 build_venv.py --mac --linux
```

### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--all` | 构建所有平台（mac、linux、win） | `python3 build_venv.py --all` |
| `--mac` | 只构建 macOS 虚拟环境 | `python3 build_venv.py --mac` |
| `--linux` | 只构建 Linux 虚拟环境 | `python3 build_venv.py --linux` |
| `--win` | 只构建 Windows 虚拟环境 | `python3 build_venv.py --win` |
| `--help` | 显示帮助信息 | `python3 build_venv.py --help` |

## 构建流程

### 详细步骤

**步骤 1/4: 创建 Python 虚拟环境**
- 检查目标目录是否已存在
- 如果存在，询问是否重新创建
- 使用 `python -m venv` 创建独立的 Python 虚拟环境

**步骤 2/4: 安装 nodeenv**
- 升级 pip 到最新版本
- 安装 `nodeenv` 包（用于在 Python 虚拟环境中嵌入 Node.js）

**步骤 3/4: 设置 Node.js 环境**
- 使用 nodeenv 下载并安装指定版本的 Node.js（默认 20.11.0）
- 将 Node.js 和 npm 嵌入到虚拟环境中
- 验证 Node.js 和 npm 版本

**步骤 4/4: 安装 Claude Code**
- 配置 npm 全局安装路径到虚拟环境
- 通过 npm 安装 `@anthropic-ai/claude-code`
- 验证 claude 命令是否可用
- 检查 node_modules 位置
- 创建便捷激活脚本（activate_claude）

**完成构建**
- 显示构建总结
- 提供下一步操作指引

### 构建输出示例

```
============================================================
🚀 Claude Code 虚拟环境构建脚本
============================================================
📂 工作目录：/Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv
🖥️  当前系统：darwin
🎯 构建目标：mac
============================================================

✅ Python 版本检查通过：3.11.5

============================================================
🔧 构建 venv_mac 虚拟环境
============================================================
ℹ️  创建虚拟环境：/Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv/venv_mac
✅ 虚拟环境创建成功：/Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv/venv_mac
ℹ️  安装 Claude Code...
ℹ️  升级 pip...
✅ pip 升级成功
ℹ️  安装 @anthropic-ai/claude-code...
✅ Claude Code 安装成功
ℹ️  验证 Claude Code 安装...
✅ Claude Code 版本：2.1.38
✅ venv_mac 构建完成！

============================================================
🎉 所有虚拟环境构建完成！
============================================================

下一步：
1. 配置环境变量：cp .env.example .env
2. 编辑 .env 文件，填入你的 API 密钥
3. 启动 Claude Code：python3 run.py
```

## 常见问题

### Q1: 提示"需要 Python 3.8 或更高版本"

**原因**: 系统 Python 版本过低

**解决方案**:
```bash
# macOS - 使用 Homebrew 安装
brew install python@3.11

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11

# Windows - 从 python.org 下载安装
# https://www.python.org/downloads/
```

### Q2: 提示"未找到 Python 命令"

**原因**: Python 未添加到 PATH 或命令名称不正确

**解决方案**:
```bash
# 尝试不同的 Python 命令
python3 build_venv.py  # macOS/Linux
python build_venv.py   # Windows

# 或使用完整路径
/usr/bin/python3 build_venv.py
```

### Q3: 虚拟环境已存在，如何重新构建？

**方案 1**: 脚本会自动询问
```
⚠️  虚拟环境已存在：/path/to/venv_mac
是否删除并重新创建？(y/N): y
```

**方案 2**: 手动删除后重建
```bash
# 删除现有虚拟环境
rm -rf venv_mac

# 重新构建
python3 build_venv.py --mac
```

### Q4: 安装 Claude Code 失败

**可能原因**:
1. 网络连接问题
2. PyPI 访问受限
3. 磁盘空间不足

**解决方案**:
```bash
# 1. 检查网络连接
ping pypi.org

# 2. 使用国内镜像（如果在中国）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 检查磁盘空间
df -h  # macOS/Linux
```

### Q5: 验证安装时超时

**原因**: Claude Code 首次运行可能需要初始化

**解决方案**:
- 这通常不影响使用
- 可以手动验证：
  ```bash
  # macOS/Linux
  ./venv_mac/bin/claude --version
  
  # Windows
  .\venv_win\Scripts\claude.exe --version
  ```

### Q6: 在 Linux 上提示缺少 python3-venv

**解决方案**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-venv

# CentOS/RHEL
sudo yum install python3-venv

# Arch Linux
sudo pacman -S python-virtualenv
```

### Q7: Windows 上提示权限错误

**解决方案**:
```powershell
# 以管理员身份运行 PowerShell
# 或者修改执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 高级用法

### 1. 批量构建多平台环境

适用于需要在多个平台分发的场景：

```bash
# 构建所有平台
python3 build_venv.py --all

# 或选择性构建
python3 build_venv.py --mac --linux
```

### 2. 自动化构建脚本

创建自动化脚本 `auto_build.sh`：

```bash
#!/bin/bash
# 自动化构建脚本

cd /path/to/claude-code-venv

# 构建虚拟环境
python3 build_venv.py --all

# 配置环境变量（如果不存在）
if [ ! -f .env ]; then
    cp .env.example .env
    echo "请编辑 .env 文件配置 API 密钥"
fi

# 打包
cd ..
tar -czf claude-code-venv-$(date +%Y%m%d).tar.gz claude-code-venv/

echo "构建完成！"
```

### 3. CI/CD 集成

在 CI/CD 流程中使用：

```yaml
# GitHub Actions 示例
name: Build Virtual Environments

on:
  push:
    branches: [ main ]

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Build virtual environment
      run: |
        cd claude-code-venv
        python build_venv.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: venv-${{ matrix.os }}
        path: claude-code-venv/venv_*
```

### 4. 自定义构建配置

修改 `build_venv.py` 中的配置：

```python
# 自定义虚拟环境名称
self.venv_configs = {
    'mac': {
        'name': 'venv_macos_arm64',  # 自定义名称
        # ...
    }
}

# 安装额外的包
def install_extra_packages(self, platform_key):
    """安装额外的 Python 包"""
    packages = ['requests', 'python-dotenv', 'rich']
    # 安装逻辑...
```

### 5. 验证构建结果

创建验证脚本 `verify_build.py`：

```python
#!/usr/bin/env python3
"""验证虚拟环境构建结果"""

import os
import sys
from pathlib import Path

def verify_venv(venv_name):
    """验证虚拟环境"""
    venv_path = Path(__file__).parent / venv_name
    
    if not venv_path.exists():
        print(f"❌ {venv_name} 不存在")
        return False
    
    # 检查关键文件
    if 'win' in venv_name:
        claude_path = venv_path / 'Scripts' / 'claude.exe'
    else:
        claude_path = venv_path / 'bin' / 'claude'
    
    if claude_path.exists():
        print(f"✅ {venv_name} 验证通过")
        return True
    else:
        print(f"❌ {venv_name} 缺少 claude 命令")
        return False

if __name__ == '__main__':
    venvs = ['venv_mac', 'venv_linux', 'venv_win']
    results = [verify_venv(v) for v in venvs]
    
    if all(results):
        print("\n🎉 所有虚拟环境验证通过！")
        sys.exit(0)
    else:
        print("\n❌ 部分虚拟环境验证失败")
        sys.exit(1)
```

## 最佳实践

### 1. 构建前准备

- ✅ 确保网络连接稳定
- ✅ 检查磁盘空间充足（至少 1GB）
- ✅ 更新 Python 到最新版本
- ✅ 清理旧的虚拟环境（如果需要）

### 2. 构建后检查

- ✅ 验证 claude 命令可用
- ✅ 检查版本号是否正确
- ✅ 测试基本功能
- ✅ 备份构建好的虚拟环境

### 3. 分发建议

- ✅ 压缩前清理缓存文件
- ✅ 不要包含 `.env` 文件（包含敏感信息）
- ✅ 提供 `.env.example` 作为配置模板
- ✅ 包含完整的使用文档

### 4. 维护建议

- ✅ 定期更新虚拟环境
- ✅ 使用 `update.py` 升级 Claude Code
- ✅ 记录构建日期和版本号
- ✅ 保留构建日志用于问题排查

## 相关文档

- [README.md](../README.md) - 项目主文档
- [UPDATE_README.md](UPDATE_README.md) - 升级说明
- [run.py](../run.py) - 启动脚本
- [update.py](../update.py) - 升级脚本

## 技术支持

如果遇到问题：

1. 查看本文档的"常见问题"部分
2. 检查构建日志中的错误信息
3. 确认系统满足所有要求
4. 尝试手动创建虚拟环境进行对比

---

**文档版本**: 1.0  
**最后更新**: 2026-02-10  
**适用版本**: Claude Code v2.1.38+
