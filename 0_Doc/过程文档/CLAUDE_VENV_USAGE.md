# Claude Code 虚拟环境使用说明

## 🎯 核心问题

虚拟环境中的 Claude Code 需要正确读取 `.venv/.claude/settings.json` 配置文件，才能连接到自定义 API 地址。

---

## ✅ 正确的使用方式

### 方式 1: 使用 run.sh 脚本（推荐）

```bash
# 直接运行（会自动设置所有环境变量）
./run.sh

# 或传递参数
./run.sh chat "你好"
./run.sh --version
```

**优点**: 
- ✅ 自动设置 `CLAUDE_CONFIG_DIR` 环境变量
- ✅ 确保使用虚拟环境中的 Claude
- ✅ 完全隔离，不影响全局配置

---

### 方式 2: 手动设置环境变量

如果你想在终端中直接使用 claude 命令：

```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 设置 Claude 配置目录（关键步骤！）
export CLAUDE_CONFIG_DIR="$PWD/.venv/.claude"

# 3. 确保使用虚拟环境中的 claude
export PATH="$PWD/.venv/bin:$PATH"

# 4. 现在可以使用了
claude chat "你好"
```

---

### 方式 3: 使用 activate_claude 脚本

```bash
# 激活虚拟环境并自动设置环境变量
source .venv/bin/activate_claude

# 然后直接使用
claude chat "你好"
```

---

## ❌ 错误的使用方式

### 错误示例 1: 只激活虚拟环境

```bash
# ❌ 错误：缺少 CLAUDE_CONFIG_DIR 环境变量
source .venv/bin/activate
claude chat "你好"  # 会尝试连接 api.anthropic.com
```

**问题**: Claude Code 会使用默认配置目录 `~/.claude/`，而不是虚拟环境中的配置。

---

### 错误示例 2: 直接运行 claude 命令

```bash
# ❌ 错误：使用全局 Claude
claude chat "你好"  # 使用全局配置
```

**问题**: 会使用全局安装的 Claude 和全局配置。

---

## 🔍 验证配置是否生效

### 检查环境变量

```bash
# 应该输出虚拟环境路径
echo $CLAUDE_CONFIG_DIR
# 期望输出: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv/.claude

# 应该输出虚拟环境中的 claude
which claude
# 期望输出: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv/bin/claude
```

### 检查配置文件

```bash
# 查看虚拟环境的配置
cat .venv/.claude/settings.json

# 应该包含:
# - ANTHROPIC_BASE_URL: https://cc.zhihuiapi.top
# - ANTHROPIC_AUTH_TOKEN: sk-rWy3...
```

---

## 📋 配置文件说明

### settings.json 位置

- **全局配置**: `~/.claude/settings.json`
- **虚拟环境配置**: `.venv/.claude/settings.json`

### 当前虚拟环境配置

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-rWy3di4jXg0VkDX8ugMMgj5t3wXzxKnfZxv0jCGeAfRY35tB",
    "ANTHROPIC_BASE_URL": "https://cc.zhihuiapi.top",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-5-20251101",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5-20250929",
    "ANTHROPIC_REASONING_MODEL": "claude-sonnet-4-5-20250929"
  },
  "enabledPlugins": {
    "rust-analyzer-lsp@claude-plugins-official": true
  }
}
```

---

## 🚀 快速开始

### 场景 1: 快速测试

```bash
./run.sh --version
```

### 场景 2: 交互式对话

```bash
./run.sh
```

### 场景 3: 在终端中持续使用

```bash
# 一次性设置
source .venv/bin/activate_claude

# 然后可以多次使用
claude chat "第一个问题"
claude chat "第二个问题"
claude --help
```

---

## 🐛 故障排查

### 问题 1: 连接 api.anthropic.com 失败

**症状**:
```
Unable to connect to Anthropic services
Failed to connect to api.anthropic.com: ERR_BAD_REQUEST
```

**原因**: Claude Code 没有读取虚拟环境的配置文件

**解决方案**:
```bash
# 方案 A: 使用 run.sh
./run.sh

# 方案 B: 手动设置环境变量
export CLAUDE_CONFIG_DIR="$PWD/.venv/.claude"
claude chat "测试"
```

---

### 问题 2: 使用了全局配置

**症状**: 虚拟环境和全局使用相同的历史记录

**检查**:
```bash
echo $CLAUDE_CONFIG_DIR
# 如果输出为空或指向 ~/.claude，说明配置错误
```

**解决方案**:
```bash
# 重新激活
source .venv/bin/activate_claude
```

---

### 问题 3: claude 命令找不到

**症状**:
```
claude: command not found
```

**检查**:
```bash
ls -la .venv/bin/claude
# 应该存在这个文件
```

**解决方案**:
```bash
# 如果文件不存在，重新安装
source .venv/bin/activate
npm config set prefix "$PWD/.venv"
npm install -g @anthropic-ai/claude-code
```

---

## 📊 环境对比

| 项目 | 全局环境 | 虚拟环境（正确配置） |
|------|---------|-------------------|
| Claude 路径 | `~/.local/bin/claude` | `.venv/bin/claude` |
| 配置目录 | `~/.claude/` | `.venv/.claude/` |
| 历史记录 | 共享 | 独立 |
| API 配置 | 全局 settings.json | 虚拟环境 settings.json |
| 可移植性 | ❌ 不可移植 | ✅ 完全可移植 |

---

## 💡 最佳实践

### 1. 始终使用 run.sh

```bash
# 推荐
./run.sh

# 而不是
claude
```

### 2. 如需在终端持续使用

```bash
# 创建别名（可选）
alias claude-venv='CLAUDE_CONFIG_DIR="$PWD/.venv/.claude" $PWD/.venv/bin/claude'

# 使用
claude-venv chat "你好"
```

### 3. 验证环境

每次使用前验证：

```bash
# 快速检查脚本
cat << 'EOF' > check_env.sh
#!/bin/bash
echo "CLAUDE_CONFIG_DIR: $CLAUDE_CONFIG_DIR"
echo "Claude 路径: $(which claude)"
echo "配置文件: $(ls -la $CLAUDE_CONFIG_DIR/settings.json 2>&1)"
EOF

chmod +x check_env.sh
./check_env.sh
```

---

## 🔗 相关文档

- [PORTABILITY_GUIDE.md](PORTABILITY_GUIDE.md) - 项目可移植性指南
- [CLAUDE_ENV_SETUP.md](CLAUDE_ENV_SETUP.md) - Claude 环境设置
- [README.md](../../README.md) - 项目主文档

---

## 📝 总结

**关键点**:
1. ✅ 使用 `./run.sh` 是最简单可靠的方式
2. ✅ 必须设置 `CLAUDE_CONFIG_DIR` 环境变量
3. ✅ 确保使用虚拟环境中的 claude 可执行文件
4. ❌ 不要直接 `source .venv/bin/activate` 后就使用 claude

**记住**: Claude Code 通过 `CLAUDE_CONFIG_DIR` 环境变量来确定配置文件位置！

---

**更新时间**: 2026-02-04  
**维护者**: Cline AI Assistant
