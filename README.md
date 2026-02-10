# Claude Code 便携式虚拟环境

> 版本：v2.1.38  
> 更新日期：2026-02-10

## 📝 项目简介

这是一个**完全独立、开箱即用**的 Claude Code 虚拟环境，包含了运行 Claude Code 所需的所有依赖。你可以将整个文件夹复制到任何位置，无需重新安装即可使用。

### ✨ 主要特性

- 🎯 **完全独立**：包含独立的 Python 虚拟环境和 Node.js 包
- 🚀 **开箱即用**：无需安装，解压即用
- 🔒 **隔离配置**：使用独立的 `.claude` 目录，不影响系统配置
- 🌍 **跨平台支持**：同时包含 macOS 和 Windows 虚拟环境
- 📦 **便携设计**：可以放在任何目录，通过全路径启动

## 📂 目录结构

```
claude-code-venv/
├── README.md              # 本文档
├── run.py                 # 启动脚本（主要使用）
├── update.py              # 升级脚本
├── VERSION                # 版本号文件
├── .env.example           # 环境变量配置示例
├── .env                   # 环境变量配置（需自行创建）
├── .claude/               # Claude 独立配置目录
│   ├── settings.json      # Claude 设置
│   └── ...                # 其他配置和缓存
├── venv_mac/              # macOS 虚拟环境
│   ├── bin/               # 可执行文件
│   └── lib/               # Python 库
├── venv_win/              # Windows 虚拟环境
│   ├── Scripts/           # 可执行文件
│   └── Lib/               # Python 库
└── doc/                   # 文档目录
    ├── UPDATE_README.md   # 升级说明
    └── ...
```

## 🚀 快速开始

### 1️⃣ 配置环境变量

首次使用前，需要配置 API 密钥：

```bash
# 1. 复制配置示例文件
cp .env.example .env

# 2. 编辑 .env 文件，填入你的 API 密钥
# 使用任何文本编辑器打开 .env 文件
# 将 ANTHROPIC_AUTH_TOKEN 的值改为你的实际 API 密钥
```

**`.env` 文件示例：**

```bash
# API 密钥（必填）
ANTHROPIC_AUTH_TOKEN=sk-ant-xxxxxxxxxxxxx

# API 基础 URL（可选）
ANTHROPIC_BASE_URL=https://api.anthropic.com

# 如果需要使用代理（可选）
# HTTP_PROXY=http://127.0.0.1:7890
# HTTPS_PROXY=http://127.0.0.1:7890
```

### 2️⃣ 启动 Claude Code

#### 方式一：在虚拟环境目录内启动

```bash
# 进入虚拟环境目录
cd /path/to/claude-code-venv

# 启动 Claude Code（工作目录为当前终端所在目录）
python3 run.py
```

#### 方式二：从任意目录启动（推荐）

**这是最灵活的使用方式！** 无论你在哪个目录，都可以通过全路径启动虚拟环境：

```bash
# 在任何项目目录下，使用全路径启动
python3 /path/to/claude-code-venv/run.py

# 例如：在你的项目目录
cd ~/my-project
python3 /Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv/run.py
```

**工作原理：**
- `run.py` 会自动检测你**当前终端所在的目录**作为工作目录
- Claude Code 会在你的项目目录中运行，而不是在虚拟环境目录
- 所有配置和依赖都使用虚拟环境中的版本

#### 方式三：创建别名（最方便）

为了更方便使用，可以在 shell 配置文件中创建别名：

**macOS/Linux (bash/zsh):**

```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
echo 'alias vclaude="python3 /Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv/run.py"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc

# 之后在任何目录都可以直接使用
cd ~/my-project
vclaude
```

**Windows (PowerShell):**

```powershell
# 编辑 PowerShell 配置文件
notepad $PROFILE

# 添加以下内容
function vclaude { python C:\path\to\claude-code-venv\run.py $args }

# 重新加载配置
. $PROFILE

# 之后在任何目录都可以直接使用
cd C:\my-project
vclaude
```

### 3️⃣ 启动信息

启动时会显示详细信息：

```
============================================================
🚀 启动 Claude Code 虚拟环境 v2.1.38
============================================================
📂 终端目录: /Users/hzk/my-project
📍 脚本目录: /Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv
📦 虚拟环境: /Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv/venv_mac
🗂️  用户目录: /Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv/.claude
🔧 Claude 路径: /Users/hzk/Documents/GitHub/hzk-claude-venv/claude-code-venv/venv_mac/bin/claude
============================================================
```

## 🔧 脚本说明

### `build_venv.py` - 虚拟环境构建脚本

**主要功能：**
- ✅ 自动检测操作系统（macOS/Linux/Windows）
- ✅ 创建 Python 虚拟环境
- ✅ 安装 nodeenv 并嵌入 Node.js 环境
- ✅ 通过 npm 安装 Claude Code
- ✅ 自动修复绝对路径，提高可移植性
- ✅ 支持选择性构建或批量构建
- ✅ 支持自定义 Node.js 版本
- ✅ 网络错误自动重试

**使用方法：**

```bash
# 进入项目目录
cd /path/to/claude-code-venv

# 构建当前系统的虚拟环境
python3 build_venv.py

# 构建所有平台的虚拟环境
python3 build_venv.py --all

# 只构建特定平台
python3 build_venv.py --mac
python3 build_venv.py --linux
python3 build_venv.py --win

# 指定 Node.js 版本
python3 build_venv.py --node-version 18.19.0

# 查看帮助
python3 build_venv.py --help
```

**构建流程：**
1. 创建 Python 虚拟环境
2. 安装 nodeenv
3. 设置 Node.js 环境
4. 安装 Claude Code
5. 修复绝对路径（提高可移植性）

**网络问题处理：**
- 自动重试 3 次
- 检测 SSL/网络错误并提供解决方案
- 支持配置代理：
  ```bash
  export HTTP_PROXY=http://127.0.0.1:7890
  export HTTPS_PROXY=http://127.0.0.1:7890
  python3 build_venv.py
  ```

**详细文档：** [BUILD_VENV_GUIDE.md](doc/BUILD_VENV_GUIDE.md)

### `run.py` - 启动脚本

**主要功能：**
- ✅ 自动检测操作系统（macOS/Windows）
- ✅ 激活对应的虚拟环境
- ✅ 加载 `.env` 文件中的环境变量
- ✅ 设置独立的 Claude 配置目录
- ✅ 在当前终端目录启动 Claude Code

**使用方法：**

```bash
# 基本启动
python3 run.py

# 传递参数给 Claude Code
python3 run.py --help
python3 run.py --version
python3 run.py --model sonnet

# 从任意目录启动（使用全路径）
python3 /path/to/claude-code-venv/run.py
```

**环境变量优先级：**
1. `.env` 文件（最高优先级）
2. `.claude/settings.json` 中的 `env` 配置
3. 系统环境变量

### `update.py` - 升级脚本

**主要功能：**
- ✅ 检查当前安装的 Claude Code 版本
- ✅ 检查是否有可用更新
- ✅ 支持选择性升级（macOS/Windows/全部）
- ✅ 显示详细的升级过程和结果

**使用方法：**

```bash
# 进入虚拟环境目录
cd /path/to/claude-code-venv

# 运行升级脚本
python3 update.py

# 按提示选择要升级的虚拟环境
# 1. macOS (推荐)
# 2. Windows
# 3. 全部升级
```

**升级流程：**
1. 扫描所有虚拟环境
2. 显示当前版本和最新版本
3. 让用户选择要升级的环境
4. 执行升级并显示进度
5. 验证升级结果

## ⚙️ 环境变量配置

### 必需配置

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `ANTHROPIC_AUTH_TOKEN` | Anthropic API 密钥 | `sk-ant-xxxxx` |

### 可选配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `ANTHROPIC_BASE_URL` | API 基础 URL | `https://api.anthropic.com` |
| `HTTP_PROXY` | HTTP 代理 | 无 |
| `HTTPS_PROXY` | HTTPS 代理 | 无 |
| `CLAUDE_CONFIG_DIR` | Claude 配置目录 | `.claude` |
| `DISABLE_AUTOUPDATER` | 禁用自动更新 | `1` |

### 模型配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku 模型版本 | `claude-haiku-4-5-20251001` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus 模型版本 | `claude-opus-4-5-20251101` |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet 模型版本 | `claude-sonnet-4-5-20250929` |
| `ANTHROPIC_REASONING_MODEL` | 推理模型版本 | `claude-sonnet-4-5-20250929` |

### 使用 cc switch 代理

如果你使用 `cc switch` 来管理 API：

```bash
ANTHROPIC_AUTH_TOKEN=PROXY_MANAGED
ANTHROPIC_BASE_URL=http://127.0.0.1:15721
```

## 🌍 跨平台使用

### macOS

虚拟环境位于 `venv_mac/` 目录，`run.py` 会自动检测并使用。

```bash
python3 run.py
```

### Windows

虚拟环境位于 `venv_win/` 目录，`run.py` 会自动检测并使用。

```bash
python run.py
```

### 同时包含两个平台

如果你需要在不同平台间共享这个虚拟环境：
- 两个虚拟环境可以共存
- `run.py` 会根据当前操作系统自动选择对应的虚拟环境
- 配置文件（`.env`、`.claude/`）在两个平台间共享

## 📦 分发和迁移

### 打包分发

1. **清理缓存**（可选）：
   ```bash
   # 如果有清理脚本
   python3 ../2_Scripts/Clear_Claude_Cache.py
   ```

2. **检查配置**：
   - 确保 `.env` 文件不包含敏感信息
   - 或者删除 `.env` 文件，只保留 `.env.example`

3. **打包**：
   ```bash
   # 压缩整个目录
   cd ..
   zip -r claude-code-venv.zip claude-code-venv/
   ```

### 迁移到新位置

1. **复制整个目录**到新位置
2. **无需重新安装**，直接使用
3. **更新别名**（如果使用了别名）

```bash
# 复制到新位置
cp -r /old/path/claude-code-venv /new/path/

# 更新别名
alias claude="python3 /new/path/claude-code-venv/run.py"
```

## 🔍 故障排除

### 问题 1：提示"虚拟环境不存在"

**原因**：虚拟环境目录缺失或损坏

**解决**：
- 检查 `venv_mac/` 或 `venv_win/` 目录是否存在
- 重新解压或复制完整的虚拟环境

### 问题 2：提示"Claude Code 未安装"

**原因**：虚拟环境中缺少 Claude Code

**解决**：
```bash
# 运行升级脚本重新安装
python3 update.py
```

### 问题 3：API 密钥错误

**原因**：`.env` 文件配置错误或未创建

**解决**：
1. 检查 `.env` 文件是否存在
2. 确认 `ANTHROPIC_AUTH_TOKEN` 配置正确
3. 确保 API 密钥有效

### 问题 4：网络连接问题

**原因**：无法访问 Anthropic API

**解决**：
- 检查网络连接
- 配置代理（如果需要）：
  ```bash
  HTTP_PROXY=http://127.0.0.1:7890
  HTTPS_PROXY=http://127.0.0.1:7890
  ```

### 问题 5：权限错误

**原因**：文件权限不足

**解决**：
```bash
# macOS/Linux
chmod +x run.py
chmod +x update.py

# 或者使用 python3 明确调用
python3 run.py
```

## 💡 使用技巧

### 1. 为不同项目使用不同配置

虽然虚拟环境是共享的，但你可以为不同项目设置不同的 Claude 配置：

```bash
# 项目 A 使用默认配置
cd ~/project-a
python3 /path/to/claude-code-venv/run.py

# 项目 B 使用自定义配置目录
cd ~/project-b
CLAUDE_CONFIG_DIR=~/project-b/.claude python3 /path/to/claude-code-venv/run.py
```

### 2. 快速切换 API 端点

在 `.env` 文件中配置多个端点，通过注释切换：

```bash
# 官方 API
ANTHROPIC_BASE_URL=https://api.anthropic.com

# 自定义代理
# ANTHROPIC_BASE_URL=http://127.0.0.1:15721

# 其他代理
# ANTHROPIC_BASE_URL=https://custom-proxy.com
```

### 3. 查看详细日志

```bash
# 启用调试模式
DEBUG=1 python3 run.py
```

### 4. 传递命令行参数

```bash
# 查看帮助
python3 run.py --help

# 指定模型
python3 run.py --model sonnet

# 查看版本
python3 run.py --version
```

## 📚 相关文档

- [UPDATE_README.md](doc/UPDATE_README.md) - 升级说明
- [UPDATE_ISSUE_ANALYSIS.md](doc/UPDATE_ISSUE_ANALYSIS.md) - 升级问题分析
- [.env.example](.env.example) - 环境变量配置示例

## 🔐 安全提示

1. **不要提交 `.env` 文件**到版本控制系统
2. **不要分享包含真实 API 密钥的配置文件**
3. **定期更换 API 密钥**
4. **使用代理时注意代理服务器的安全性**

## 📝 版本历史

### v2.1.38 (2026-02-10)
- ✨ 当前版本
- ✅ 支持从任意目录启动
- ✅ 完善的环境变量配置
- ✅ 跨平台支持

## 🤝 贡献

如果你发现问题或有改进建议，欢迎反馈！

## 📄 许可证

本项目遵循相关开源许可证。

---

**最后更新**: 2026-02-10  
**维护者**: hzk-claude-venv 项目组
