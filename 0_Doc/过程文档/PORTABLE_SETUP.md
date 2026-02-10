# 可移植虚拟环境设置指南

## 🎯 目标

创建一个可以打包到其他电脑上使用的 Claude Code 环境，通过 `run.*` 脚本作为唯一入口。

## ⚠️ Python 虚拟环境的限制

**重要**：Python 的 `venv` 模块创建的虚拟环境**不是可移植的**，因为：

1. 虚拟环境中的 Python 解释器路径是硬编码的绝对路径
2. pip、setuptools 等工具也包含绝对路径
3. 这是 Python venv 的设计决策，无法轻易改变

## ✅ 推荐方案：使用 run 脚本 + 本地安装

### 方案 A：仅打包 Claude Code（推荐）

**适用场景**：目标电脑已有 Python 和 Node.js

#### 打包内容

```
aigc-film-agent/
├── run.py              # Python 启动脚本
├── run.sh              # Bash 启动脚本
├── run.bat             # Windows 启动脚本
├── setup.sh            # 自动安装脚本（新建）
├── setup.bat           # Windows 自动安装脚本（新建）
├── requirements.txt    # Python 依赖（如果有）
└── docs/               # 文档
```

#### 使用流程

1. 将项目复制到目标电脑
2. 运行 `./setup.sh`（或 `setup.bat`）自动创建虚拟环境
3. 使用 `./run.sh` 启动 Claude Code

### 方案 B：使用 Docker（完全可移植）

**适用场景**：需要完全一致的环境

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

# 安装 Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Claude Code
RUN npm install -g @anthropic-ai/claude-code

# 设置独立的用户目录
ENV CLAUDE_CONFIG_DIR=/app/.claude

CMD ["claude"]
```

### 方案 C：使用便携式 Python + Node.js

**适用场景**：目标电脑没有 Python/Node.js

使用便携式版本：
- **Python**: [WinPython](https://winpython.github.io/) (Windows) 或 [Python Embedded](https://www.python.org/downloads/)
- **Node.js**: [Node.js Portable](https://nodejs.org/en/download/)

## 🚀 实现方案 A：自动安装脚本

我将创建 `setup.sh` 和 `setup.bat` 脚本，让用户在新电脑上一键安装。

### 工作流程

```bash
# 在新电脑上
git clone <your-repo>
cd aigc-film-agent

# 运行安装脚本
./setup.sh

# 使用
./run.sh
```

## 📦 打包清单

### 需要打包的文件

```
✅ run.py
✅ run.sh
✅ run.bat
✅ setup.sh (新建)
✅ setup.bat (新建)
✅ README.md
✅ docs/
✅ .gitignore
```

### 不需要打包的文件

```
❌ .venv/          # 虚拟环境（包含绝对路径）
❌ node_modules/   # npm 包
❌ .claude/        # 用户配置
❌ __pycache__/    # Python 缓存
```

## 🔧 Git 配置

确保 `.gitignore` 包含：

```gitignore
.venv/
node_modules/
.claude/
__pycache__/
*.pyc
.DS_Store
```

## 📝 使用说明

### 在源电脑上

```bash
# 1. 提交代码（不包含 .venv）
git add .
git commit -m "Add portable setup scripts"
git push
```

### 在目标电脑上

```bash
# 1. 克隆项目
git clone <your-repo>
cd aigc-film-agent

# 2. 运行安装脚本
./setup.sh

# 3. 使用 Claude Code
./run.sh
```

## 🎯 下一步

我将创建：
1. `setup.sh` - macOS/Linux 自动安装脚本
2. `setup.bat` - Windows 自动安装脚本
3. 更新 `README.md` 添加使用说明

这样你就可以：
- ✅ 将项目打包（不包含 .venv）
- ✅ 在新电脑上运行 setup 脚本自动安装
- ✅ 使用 run 脚本启动，无需手动配置

---

**创建时间**: 2026-02-04
