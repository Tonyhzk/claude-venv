# Claude Code 工作目录说明

## 概述

Claude Code 启动脚本现在支持**智能工作目录检测**，能够区分两个重要的目录：

1. **终端当前目录**：用户执行脚本时所在的目录（Claude Code 的工作目录）
2. **脚本所在目录**：虚拟环境和配置文件的存储位置

## 工作原理

### 目录检测机制

```
终端当前目录 (CURRENT_DIR)
    ↓
    用户在这里执行命令
    ↓
脚本所在目录 (SCRIPT_DIR)
    ├── .venv/              # 虚拟环境
    │   ├── bin/claude      # Claude Code 可执行文件
    │   └── .claude/        # 配置和用户数据
    ├── run.py              # Python 启动脚本
    └── run.sh              # Shell 启动脚本
```

### 执行流程

1. **检测终端目录**：脚本获取用户执行命令时所在的目录
2. **定位虚拟环境**：脚本找到自身所在目录下的 `.venv`
3. **加载配置**：从 `.venv/.claude/settings.json` 读取配置
4. **启动 Claude**：在终端目录中启动 Claude Code

## 使用场景

### 场景 1：在项目根目录启动

```bash
# 当前位置：/Users/hzk/Documents/GitHub/aigc-film-agent
./claude-code-venv/run.py
```

**结果**：
- 📂 终端目录：`/Users/hzk/Documents/GitHub/aigc-film-agent`
- 📍 脚本目录：`/Users/hzk/Documents/GitHub/aigc-film-agent/claude-code-venv`
- Claude Code 工作在 `aigc-film-agent` 目录

### 场景 2：在任意子目录启动

```bash
# 当前位置：/Users/hzk/Documents/GitHub/aigc-film-agent/0_Doc
../claude-code-venv/run.py
```

**结果**：
- 📂 终端目录：`/Users/hzk/Documents/GitHub/aigc-film-agent/0_Doc`
- 📍 脚本目录：`/Users/hzk/Documents/GitHub/aigc-film-agent/claude-code-venv`
- Claude Code 工作在 `0_Doc` 目录

### 场景 3：在完全不同的项目中启动

```bash
# 当前位置：/Users/hzk/Documents/GitHub/another-project
/Users/hzk/Documents/GitHub/aigc-film-agent/claude-code-venv/run.py
```

**结果**：
- 📂 终端目录：`/Users/hzk/Documents/GitHub/another-project`
- 📍 脚本目录：`/Users/hzk/Documents/GitHub/aigc-film-agent/claude-code-venv`
- Claude Code 工作在 `another-project` 目录
- 但使用 `aigc-film-agent` 的虚拟环境和配置

## 优势

### 1. 灵活性
- ✅ 可以在任何目录启动 Claude Code
- ✅ 不需要切换到特定目录
- ✅ 支持多项目使用同一个虚拟环境

### 2. 配置复用
- ✅ 虚拟环境和配置集中管理
- ✅ API 密钥等敏感信息统一存储
- ✅ 多个项目共享相同的 Claude Code 配置

### 3. 便捷性
- ✅ 无需每次都 cd 到特定目录
- ✅ 可以创建全局别名快速启动
- ✅ 支持从任何位置访问

## 创建全局别名（可选）

### macOS/Linux

在 `~/.zshrc` 或 `~/.bashrc` 中添加：

```bash
# Claude Code 快速启动别名
alias claude-venv='/Users/hzk/Documents/GitHub/aigc-film-agent/claude-code-venv/run.py'
```

使用方法：
```bash
# 在任何目录直接执行
cd ~/my-project
claude-venv
```

### 创建符号链接

```bash
# 创建到用户 bin 目录的符号链接
ln -s /Users/hzk/Documents/GitHub/aigc-film-agent/claude-code-venv/run.py ~/.local/bin/claude-venv

# 确保 ~/.local/bin 在 PATH 中
export PATH="$HOME/.local/bin:$PATH"
```

使用方法：
```bash
# 在任何目录直接执行
cd ~/any-project
claude-venv
```

## 技术实现

### Python 脚本 (run.py)

```python
# 获取脚本所在目录（虚拟环境目录）
script_dir = Path(__file__).parent.absolute()
venv_path = script_dir / ".venv"

# 获取终端当前工作目录（用户执行脚本时所在的目录）
current_dir = Path.cwd().absolute()

# 启动 Claude Code（工作目录为终端当前目录）
result = subprocess.run(
    [str(claude_bin)] + claude_args,
    env=env,
    cwd=str(current_dir)  # 关键：使用终端当前目录
)
```

### Shell 脚本 (run.sh)

```bash
# 获取脚本所在目录（虚拟环境目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/.venv"

# 获取终端当前工作目录（用户执行脚本时所在的目录）
CURRENT_DIR="$(pwd)"

# 启动 Claude Code（工作目录为终端当前目录）
cd "$CURRENT_DIR"
exec "$CLAUDE_BIN" "$@"
```

## 注意事项

### 1. 配置文件位置
- 配置文件始终在：`<脚本目录>/.venv/.claude/settings.json`
- 不会随工作目录变化而改变

### 2. 虚拟环境隔离
- 每个虚拟环境的配置是独立的
- 不同项目可以有不同的虚拟环境和配置

### 3. 权限问题
- 确保脚本有执行权限：`chmod +x run.py run.sh`
- 确保虚拟环境目录可访问

## 常见问题

### Q: Claude Code 会在哪个目录工作？
A: Claude Code 会在**你执行脚本时所在的目录**工作，而不是脚本所在的目录。

### Q: 配置文件在哪里？
A: 配置文件在**脚本所在目录**的 `.venv/.claude/` 下，不会随工作目录变化。

### Q: 可以在多个项目中使用同一个虚拟环境吗？
A: 可以！只要从不同目录执行同一个启动脚本即可。

### Q: 如何查看当前使用的目录？
A: 启动时会显示：
```
📂 终端目录: /path/to/your/current/directory
📍 脚本目录: /path/to/claude-code-venv
```

## 相关文档

- [快速开始指南](QUICK_START_GUIDE.md)
- [虚拟环境使用说明](CLAUDE_VENV_USAGE.md)
- [便携性指南](PORTABILITY_GUIDE.md)
