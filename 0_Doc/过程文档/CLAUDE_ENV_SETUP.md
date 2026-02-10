# Claude Code 虚拟环境配置说明

## 📋 概述

本项目已配置独立的 Claude Code 虚拟环境，与系统全局安装完全隔离。

## 🎯 环境信息

| 项目 | 配置 |
|------|------|
| Python 虚拟环境 | `.venv/` |
| Node.js 版本 | v24.9.0 |
| npm 版本 | 11.6.0 |
| Claude Code 版本 | 2.1.29 |
| npm 全局路径 | `.venv/` (项目内) |

## 🚀 使用方法

### 方法 1：使用便捷脚本（推荐）

```bash
source .venv/bin/activate_claude
```

此脚本会自动：
- ✅ 激活 Python 虚拟环境
- ✅ 配置 npm 全局路径到虚拟环境
- ✅ 确保 PATH 优先级正确
- ✅ 显示环境信息

### 方法 2：手动激活

```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 验证 Claude Code 路径
which claude
# 应输出: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv/bin/claude

# 3. 验证版本
claude --version
```

## ✅ 验证环境隔离

运行以下命令确认环境隔离正确：

```bash
# 在虚拟环境中
source .venv/bin/activate_claude

# 检查 claude 命令路径
which claude
# ✅ 应该指向: .venv/bin/claude

# 检查 npm 全局包安装位置
npm list -g --depth=0
# ✅ 应该显示: .venv/lib

# 检查 npm prefix
npm config get prefix
# ✅ 应该显示: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv
```

## 🔧 环境配置详情

### npm 配置

```bash
# npm 全局安装路径已设置为虚拟环境
npm config get prefix
# 输出: /Users/hzk/Documents/GitHub/aigc-film-agent/.venv
```

### PATH 优先级

```
1. .venv/bin                    # 虚拟环境（最高优先级）
2. ~/.local/bin                 # 用户本地
3. /opt/homebrew/bin            # Homebrew
```

## 📦 安装的包

### Python 包
- nodeenv==1.10.0

### npm 全局包（虚拟环境内）
- @anthropic-ai/claude-code@2.1.29

## 🛠️ 维护操作

### 更新 Claude Code

```bash
source .venv/bin/activate_claude
npm update -g @anthropic-ai/claude-code
```

### 重新安装 Claude Code

```bash
source .venv/bin/activate
npm uninstall -g @anthropic-ai/claude-code
npm install -g @anthropic-ai/claude-code
```

### 清理虚拟环境

```bash
# 删除虚拟环境
rm -rf .venv

# 重新创建
python3 -m venv .venv
source .venv/bin/activate
pip install nodeenv
nodeenv --node=24.9.0 --prebuilt .
npm config set prefix "$PWD/.venv"
npm install -g @anthropic-ai/claude-code
```

## ⚠️ 注意事项

1. **环境隔离**：虚拟环境中的 Claude Code 与全局安装完全独立
2. **激活必需**：每次使用前必须激活虚拟环境
3. **npm 配置**：npm prefix 已永久设置到虚拟环境，无需每次配置
4. **版本管理**：可以在虚拟环境中使用不同版本的 Claude Code

## 🐛 故障排查

### 问题：`which claude` 仍指向全局路径

**解决方案**：
```bash
# 重新激活环境
source .venv/bin/activate_claude

# 或手动设置 PATH
export PATH="$PWD/.venv/bin:$PATH"
```

### 问题：npm 安装到了错误的位置

**解决方案**：
```bash
# 检查 npm prefix
npm config get prefix

# 如果不正确，重新设置
npm config set prefix "$PWD/.venv"
```

### 问题：nodeenv 报错 `--relocatable` 参数不存在

**解决方案**：
```bash
# nodeenv 1.10.0 已移除此参数，直接使用：
nodeenv --node=24.9.0 --prebuilt .
```

## 📚 相关文档

- [Claude Code 官方文档](https://docs.anthropic.com/claude/docs)
- [nodeenv 文档](https://github.com/ekalinin/nodeenv)
- [npm 配置文档](https://docs.npmjs.com/cli/v9/using-npm/config)

---

**最后更新**: 2026-02-04
