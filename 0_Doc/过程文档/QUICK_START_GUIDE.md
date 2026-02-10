# Claude Code 虚拟环境快速开始指南

## 🎯 虚拟环境已配置完成！

你的 Claude Code 虚拟环境已经设置完毕，现在可以开始使用了。

## 📋 当前配置状态

### ✅ 已完成的配置

1. **虚拟环境创建**: `.venv/` 目录
2. **Claude Code 安装**: 安装在虚拟环境中（`.venv/lib/node_modules/`）
3. **激活脚本**: `.venv/bin/activate_claude`
4. **独立用户目录**: 配置了 `CLAUDE_CONFIG_DIR` 环境变量
5. **清理完成**: 删除了项目根目录的 `node_modules/`、`package.json` 和 `package-lock.json`

### 📊 环境信息

```
Python: 3.11.0
Node.js: v24.9.0
npm: 11.6.0
Claude Code: 2.1.29
```

## 🚀 使用方法

### 1. 激活虚拟环境

每次使用 Claude Code 前，先激活虚拟环境：

```bash
source .venv/bin/activate_claude
```

**激活后你会看到**：
```
✅ Claude Code 虚拟环境已激活（独立用户目录模式）
📍 Claude 路径: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv/bin/claude
📦 Claude 版本: 2.1.29 (Claude Code)
🗂️  用户目录: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv/.claude

💡 提示: 此环境使用独立的配置和历史记录，与全局 ~/.claude/ 完全隔离
```

### 2. 使用 Claude Code

激活后直接使用：

```bash
# 启动 Claude Code
claude

# 查看版本
claude --version

# 查看帮助
claude --help

# 查看 MCP 服务器
claude mcp list
```

### 3. 退出虚拟环境

```bash
deactivate
```

## 🎨 特性说明

### ✨ 独立用户目录模式

你的虚拟环境现在使用**独立的用户目录**，这意味着：

| 功能 | 全局目录 | 虚拟环境目录 |
|------|---------|------------|
| **配置文件** | `~/.claude/settings.json` | `.venv/.claude/settings.json` |
| **对话历史** | `~/.claude/history.jsonl` | `.venv/.claude/history.jsonl` |
| **MCP 配置** | `~/.claude/.mcp.json` | `.venv/.claude/.mcp.json` |
| **权限设置** | `~/.claude/permissions.json` | `.venv/.claude/permissions.json` |
| **项目数据** | `~/.claude/projects/` | `.venv/.claude/projects/` |

**优势**：
- ✅ 完全隔离：虚拟环境的配置不会影响全局配置
- ✅ 项目独立：每个项目可以有自己的设置和历史
- ✅ 易于清理：删除 `.venv/` 即可清除所有数据
- ✅ 团队协作：可以共享虚拟环境配置（通过 Git）

### 🔄 如何切换模式

如果你想**临时使用全局配置**，可以：

```bash
# 方法 1：使用标准的 Python 虚拟环境激活（不设置 CLAUDE_CONFIG_DIR）
source .venv/bin/activate

# 方法 2：取消 CLAUDE_CONFIG_DIR 环境变量
unset CLAUDE_CONFIG_DIR
```

如果你想**永久使用全局配置**，编辑 `.venv/bin/activate_claude`，注释掉这一行：

```bash
# export CLAUDE_CONFIG_DIR="$VIRTUAL_ENV/.claude"
```

## 📁 目录结构

```
aigc-film-agent/
├── .venv/                          # Python 虚拟环境
│   ├── bin/
│   │   ├── activate               # Python 虚拟环境激活脚本
│   │   ├── activate_claude        # Claude Code 激活脚本（推荐使用）
│   │   ├── claude                 # Claude Code 可执行文件
│   │   ├── python                 # Python 解释器
│   │   └── npm                    # npm 包管理器
│   ├── lib/
│   │   └── node_modules/          # npm 包（包括 Claude Code）
│   │       └── @anthropic-ai/
│   │           └── claude-code/
│   └── .claude/                   # 独立的用户目录（使用 activate_claude 时）
│       ├── settings.json          # 虚拟环境的配置
│       ├── history.jsonl          # 虚拟环境的对话历史
│       ├── .mcp.json              # 虚拟环境的 MCP 配置
│       └── ...                    # 其他配置文件
├── docs/                          # Claude Code 官方文档
├── CLAUDE_ENV_SETUP.md            # 环境设置说明
├── CLAUDE_USER_DIRECTORY.md       # 用户目录详细说明
├── NODE_MODULES_EXPLANATION.md    # node_modules 问题说明
├── VIRTUAL_ENV_PATH_EXPLANATION.md # 虚拟环境路径说明
├── QUICK_START_GUIDE.md           # 本文件
├── README.md                      # 项目说明
└── .gitignore                     # Git 忽略配置
```

## 🛠️ 常见任务

### 更新 Claude Code

```bash
# 激活虚拟环境
source .venv/bin/activate_claude

# 更新到最新版本
npm install -g @anthropic-ai/claude-code@latest

# 验证版本
claude --version
```

### 安装其他 npm 包

```bash
# 激活虚拟环境
source .venv/bin/activate_claude

# 安装包（会安装到 .venv/lib/node_modules/）
npm install -g <package-name>
```

### 查看虚拟环境信息

```bash
# 激活虚拟环境
source .venv/bin/activate_claude

# 查看 npm 全局包
npm list -g --depth=0

# 查看 npm 配置
npm config get prefix
# 应该输出: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv

# 查看 PATH
echo $PATH | tr ':' '\n' | head -5

# 查看用户目录
echo $CLAUDE_CONFIG_DIR
# 应该输出: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv/.claude
```

### 清理虚拟环境

```bash
# 完全删除虚拟环境
rm -rf .venv/

# 重新创建（参考 CLAUDE_ENV_SETUP.md）
python -m venv .venv
source .venv/bin/activate_claude
npm install -g @anthropic-ai/claude-code
```

## ⚠️ 注意事项

### 1. 始终先激活虚拟环境

```bash
# ❌ 错误：直接运行（会使用全局的 Claude Code）
claude

# ✅ 正确：先激活虚拟环境
source .venv/bin/activate_claude
claude
```

### 2. 不要在项目根目录运行 npm install

```bash
# ❌ 错误：会在项目根目录创建 node_modules/
npm install

# ✅ 正确：先激活虚拟环境，然后使用 -g 标志
source .venv/bin/activate_claude
npm install -g @anthropic-ai/claude-code
```

### 3. 检查 npm prefix

如果发现包没有安装到虚拟环境，检查 npm prefix：

```bash
source .venv/bin/activate_claude
npm config get prefix

# 应该输出虚拟环境路径，而不是 /opt/homebrew 或 /usr/local
```

如果不正确，手动设置：

```bash
npm config set prefix "$PWD/.venv"
```

## 🔗 相关文档

- **CLAUDE_ENV_SETUP.md** - 详细的环境设置步骤
- **CLAUDE_USER_DIRECTORY.md** - 用户目录结构和配置说明
- **NODE_MODULES_EXPLANATION.md** - node_modules 位置问题解释
- **VIRTUAL_ENV_PATH_EXPLANATION.md** - 虚拟环境路径说明
- **docs/** - Claude Code 官方文档

## 💡 提示

### 创建别名（可选）

为了更方便使用，可以在 `~/.zshrc` 或 `~/.bashrc` 中添加别名：

```bash
# 添加到 ~/.zshrc
alias activate-claude='source .venv/bin/activate_claude'
```

然后重新加载配置：

```bash
source ~/.zshrc
```

现在可以使用：

```bash
activate-claude
```

### VS Code 集成

如果你使用 VS Code，可以配置终端自动激活虚拟环境：

1. 打开 VS Code 设置（`Cmd+,`）
2. 搜索 "terminal integrated env"
3. 添加配置：

```json
{
  "terminal.integrated.env.osx": {
    "CLAUDE_CONFIG_DIR": "${workspaceFolder}/.venv/.claude"
  }
}
```

## 🎉 开始使用

现在你可以开始使用 Claude Code 了！

```bash
# 激活虚拟环境
source .venv/bin/activate_claude

# 启动 Claude Code
claude

# 享受编程！
```

---

**最后更新**: 2026-02-04
**虚拟环境版本**: Python 3.11.0, Node.js v24.9.0, Claude Code 2.1.29
