# Claude Code 用户目录说明

## 📍 重要发现

**Claude Code 的用户配置和数据目录是全局共享的**，即使在虚拟环境中运行，也使用相同的用户目录。

## 🗂️ 用户目录结构

### 主配置目录：`~/.claude/`

这是 Claude Code 的主要用户数据目录，包含：

```
~/.claude/
├── .mcp.json                    # MCP 服务器配置
├── history.jsonl                # 对话历史记录
├── settings.json                # 用户设置
├── permissions.json             # 权限配置
├── projects/                    # 项目相关数据
├── file-history/                # 文件历史记录
├── debug/                       # 调试日志
├── cache/                       # 缓存数据
├── chrome/                      # Chrome 集成数据
├── downloads/                   # 下载文件
├── hooks/                       # 钩子脚本
├── ide/                         # IDE 集成数据
├── paste-cache/                 # 粘贴缓存
├── plans/                       # 计划数据
├── plugins/                     # 插件数据
├── session-env/                 # 会话环境
├── shell-snapshots/             # Shell 快照
├── tasks/                       # 任务数据
├── telemetry/                   # 遥测数据
├── todos/                       # 待办事项
└── statsig/                     # 统计数据
```

### 状态目录：`~/.local/state/claude/`

```
~/.local/state/claude/
└── locks/                       # 锁文件
```

### 共享数据目录：`~/.local/share/claude/`

```
~/.local/share/claude/
└── versions/                    # 版本信息
```

### 其他相关目录

```
~/Library/Caches/claude-cli-nodejs/          # Node.js CLI 缓存
~/Library/WebKit/com.claudecode.permission-manager/  # 权限管理器
~/Library/Caches/com.claudecode.permission-manager/  # 权限管理器缓存
~/.cache/claude/                             # 通用缓存
```

## 🔍 关键配置文件

### 1. MCP 配置：`~/.claude/.mcp.json`

MCP 服务器配置文件，定义了可用的 MCP 服务器。

**当前配置的 MCP 服务器**：
- ✅ dida365
- ❌ fetch (连接失败)
- ✅ mcp-playwright
- ❌ perplexity (连接失败)
- ✅ postgres-manager

### 2. 用户设置：`~/.claude/settings.json`

包含 Claude Code 的所有用户偏好设置。

### 3. 权限配置：`~/.claude/permissions.json`

存储工具和目录的权限设置。

### 4. 对话历史：`~/.claude/history.jsonl`

所有对话的历史记录（JSONL 格式）。

## ⚠️ 重要说明

### 环境隔离的范围

| 项目 | 是否隔离 | 说明 |
|------|---------|------|
| Claude Code 可执行文件 | ✅ 隔离 | 虚拟环境：`.venv/bin/claude` |
| npm 包 | ✅ 隔离 | 虚拟环境：`.venv/lib/node_modules/` |
| Node.js 版本 | ✅ 隔离 | 虚拟环境使用独立的 Node.js |
| **用户配置和数据** | ❌ **共享** | 所有环境共用 `~/.claude/` |
| **对话历史** | ❌ **共享** | 所有环境共用 `~/.claude/history.jsonl` |
| **MCP 配置** | ❌ **共享** | 所有环境共用 `~/.claude/.mcp.json` |

### 为什么用户目录是共享的？

这是 Claude Code 的设计决策：
1. **用户体验一致性**：无论在哪个项目中使用，配置和历史都保持一致
2. **数据持久性**：对话历史和设置不会因切换项目而丢失
3. **简化管理**：只需维护一套配置，而不是每个项目一套

## 🛠️ 如何实现完全隔离（高级）

如果你确实需要为虚拟环境创建独立的用户目录，可以通过环境变量实现：

### ✅ 方法 1：使用 CLAUDE_CONFIG_DIR 环境变量（官方支持）

**根据官方文档，Claude Code 支持 `CLAUDE_CONFIG_DIR` 环境变量来自定义配置和数据文件的存储位置。**

修改 `.venv/bin/activate_claude` 脚本：

```bash
#!/bin/bash
# 激活 Python 虚拟环境
source "$(dirname "$0")/activate"

# 设置 npm 全局安装路径到虚拟环境
export NPM_CONFIG_PREFIX="$VIRTUAL_ENV"

# 🎯 设置独立的 Claude 用户目录（官方支持）
export CLAUDE_CONFIG_DIR="$VIRTUAL_ENV/.claude"

# 确保虚拟环境的 bin 目录在 PATH 最前面
export PATH="$VIRTUAL_ENV/bin:$PATH"

# 创建独立的配置目录
mkdir -p "$CLAUDE_CONFIG_DIR"

echo "✅ Claude Code 虚拟环境已激活（独立用户目录）"
echo "📍 Claude 路径: $(which claude)"
echo "📦 Claude 版本: $(claude --version)"
echo "🗂️  用户目录: $CLAUDE_CONFIG_DIR"
echo ""
echo "💡 提示: 此环境使用独立的配置和历史记录"
```

**这个方法的优势：**
- ✅ 官方文档明确支持
- ✅ 完全隔离配置、历史记录、MCP 服务器等所有数据
- ✅ 不会影响全局的 `~/.claude/` 目录
- ✅ 每个虚拟环境可以有独立的设置

### 方法 2：使用项目级配置（部分隔离）

Claude Code 支持项目级配置，可以在项目根目录创建 `.claude/` 目录：

```bash
mkdir -p .claude
# 在项目目录中创建项目特定的配置
```

**注意**：这种方法只能隔离项目级别的配置（如 settings.json、agents、skills 等），但对话历史和 MCP 配置仍然是全局共享的。

## 📊 用户目录大小

当前用户目录占用空间：

```bash
# 查看主目录大小
du -sh ~/.claude/
# 示例输出：约 800KB - 几百MB（取决于使用情况）

# 查看历史文件大小
ls -lh ~/.claude/history.jsonl
# 示例输出：约 761KB
```

## 🧹 清理建议

### 清理缓存

```bash
# 清理缓存（不影响配置和历史）
rm -rf ~/.claude/cache/*
rm -rf ~/.claude/paste-cache/*
rm -rf ~/Library/Caches/claude-cli-nodejs/*
```

### 备份重要数据

```bash
# 备份配置和历史
cp ~/.claude/settings.json ~/claude-settings-backup.json
cp ~/.claude/history.jsonl ~/claude-history-backup.jsonl
cp ~/.claude/.mcp.json ~/claude-mcp-backup.json
```

## 🔗 相关路径速查

| 用途 | 默认路径 | 自定义路径（使用 CLAUDE_CONFIG_DIR） |
|------|---------|-----------------------------------|
| 主配置目录 | `~/.claude/` | `$CLAUDE_CONFIG_DIR/` |
| MCP 配置 | `~/.claude/.mcp.json` | `$CLAUDE_CONFIG_DIR/.mcp.json` |
| 用户设置 | `~/.claude/settings.json` | `$CLAUDE_CONFIG_DIR/settings.json` |
| 对话历史 | `~/.claude/history.jsonl` | `$CLAUDE_CONFIG_DIR/history.jsonl` |
| 权限配置 | `~/.claude/permissions.json` | `$CLAUDE_CONFIG_DIR/permissions.json` |
| 项目数据 | `~/.claude/projects/` | `$CLAUDE_CONFIG_DIR/projects/` |
| 调试日志 | `~/.claude/debug/` | `$CLAUDE_CONFIG_DIR/debug/` |
| 虚拟环境可执行文件 | `.venv/bin/claude` | `.venv/bin/claude` |
| 虚拟环境 npm 包 | `.venv/lib/node_modules/@anthropic-ai/claude-code/` | `.venv/lib/node_modules/@anthropic-ai/claude-code/` |

## 📚 官方文档参考

- **环境变量文档**: [Settings - Environment variables](https://code.claude.com/docs/settings#environment-variables)
- **CLAUDE_CONFIG_DIR**: 官方支持的环境变量，用于自定义 Claude Code 配置和数据文件的存储位置

---

**最后更新**: 2026-02-04
