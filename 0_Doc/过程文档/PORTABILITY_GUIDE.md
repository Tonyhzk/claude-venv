# 项目可移植性指南

**更新时间**: 2026-02-04  
**状态**: ✅ 已完成绝对路径修复

---

## 📋 概述

本项目已经过完整的可移植性优化，可以安全地：
- ✅ 移动到任意目录
- ✅ 复制到其他机器
- ✅ 打包分发
- ✅ 在不同用户环境下运行

**核心原则**: 所有路径由 `run.sh` / `run.py` / `run.bat` 启动脚本动态计算和传递。

---

## 🎯 已修复的问题

### 1. 虚拟环境绝对路径

| 文件类型 | 修复前 | 修复后 | 状态 |
|---------|--------|--------|------|
| `activate` | 硬编码绝对路径 | 动态检测路径 | ✅ |
| `activate.fish` | 硬编码绝对路径 | 动态检测路径 | ✅ |
| `activate.csh` | 硬编码绝对路径 | 动态检测路径 | ✅ |
| `Activate.ps1` | 硬编码绝对路径 | 动态检测路径 | ✅ |
| `pip/pip3/pip3.11` | `#!/绝对路径/python` | `#!/usr/bin/env python` | ✅ |
| `nodeenv` | `#!/绝对路径/python` | `#!/usr/bin/env python` | ✅ |

### 2. 配置文件

| 文件 | 说明 | 可移植性 |
|------|------|---------|
| `pyvenv.cfg` | 虚拟环境元数据，包含创建时的路径 | ⚠️ 仅供参考，不影响运行 |
| `.venv/bin/python` | 二进制文件，链接到系统 Python | ✅ 自动适配 |

---

## 🚀 使用方法

### 启动项目

**推荐方式**（跨平台）：

```bash
# macOS/Linux
./run.sh

# Windows
run.bat

# 或使用 Python 脚本（所有平台）
python run.py
```

**传递参数**：

```bash
./run.sh --version
./run.sh --help
./run.sh chat "你好"
```

### 环境变量说明

启动脚本会自动设置以下环境变量：

| 环境变量 | 说明 | 示例值 |
|---------|------|--------|
| `VIRTUAL_ENV` | 虚拟环境路径 | `<项目路径>/.venv` |
| `CLAUDE_CONFIG_DIR` | Claude 配置目录 | `<项目路径>/.venv/.claude` |
| `NPM_CONFIG_PREFIX` | npm 全局安装路径 | `<项目路径>/.venv` |
| `PATH` | 可执行文件搜索路径 | `<项目路径>/.venv/bin:...` |

---

## 📦 打包和分发

### 方法 1: 直接打包（推荐）

```bash
# 1. 确保 .gitignore 正确配置（已配置）
cat .gitignore | grep -E "(\.venv|node_modules)"

# 2. 打包整个项目（包含 .venv）
tar -czf aigc-film-agent.tar.gz \
    --exclude='.git' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.DS_Store' \
    .

# 3. 在目标机器解压
tar -xzf aigc-film-agent.tar.gz
cd aigc-film-agent

# 4. 直接运行（无需重新创建虚拟环境）
./run.sh --version
```

### 方法 2: 仅打包源代码

```bash
# 1. 导出依赖列表
source .venv/bin/activate
pip freeze > requirements.txt
npm list -g --depth=0 > npm-packages.txt

# 2. 打包源代码（不包含 .venv）
tar -czf aigc-film-agent-src.tar.gz \
    --exclude='.venv' \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    .

# 3. 在目标机器重建环境
tar -xzf aigc-film-agent-src.tar.gz
cd aigc-film-agent

# 创建虚拟环境
python3 -m venv .venv

# 激活并安装依赖
source .venv/bin/activate
pip install -r requirements.txt
npm config set prefix "$PWD/.venv"
npm install -g @anthropic-ai/claude-code

# 运行
./run.sh --version
```

---

## 🔧 维护和更新

### 添加新的 Python 包

```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 安装包
pip install <package-name>

# 3. 更新 requirements.txt
pip freeze > requirements.txt
```

### 添加新的 npm 包

```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 确保 npm prefix 正确
npm config set prefix "$PWD/.venv"

# 3. 安装包
npm install -g <package-name>
```

### 重新修复绝对路径

如果重新创建了虚拟环境，运行修复脚本：

```bash
./fix_venv_paths.sh
```

---

## ✅ 验证可移植性

### 测试 1: 本地移动

```bash
# 1. 移动项目到新位置
mv /path/to/aigc-film-agent /new/path/aigc-film-agent

# 2. 进入新位置
cd /new/path/aigc-film-agent

# 3. 验证运行
./run.sh --version
```

### 测试 2: 复制到其他机器

```bash
# 在源机器
tar -czf aigc-film-agent.tar.gz aigc-film-agent/

# 在目标机器
tar -xzf aigc-film-agent.tar.gz
cd aigc-film-agent
./run.sh --version
```

### 测试 3: 检查绝对路径

```bash
# 应该返回 "✅ 所有硬编码绝对路径已清除"
grep -r "/Users/hzk/Documents/GitHub/aigc-film-agent" .venv/bin/ 2>/dev/null || \
    echo "✅ 所有硬编码绝对路径已清除"
```

---

## 🐛 故障排查

### 问题 1: 虚拟环境激活失败

**症状**: `source .venv/bin/activate` 报错

**解决方案**:
```bash
# 不要直接激活，使用启动脚本
./run.sh
```

### 问题 2: pip 找不到 Python

**症状**: `pip: command not found` 或 `bad interpreter`

**解决方案**:
```bash
# 重新运行修复脚本
./fix_venv_paths.sh

# 或通过启动脚本运行
./run.sh
```

### 问题 3: Claude 找不到

**症状**: `claude: command not found`

**解决方案**:
```bash
# 检查 Claude 是否安装在虚拟环境中
ls -la .venv/bin/claude

# 如果不存在，重新安装
source .venv/bin/activate
npm config set prefix "$PWD/.venv"
npm install -g @anthropic-ai/claude-code
```

### 问题 4: 移动后路径错误

**症状**: 仍然引用旧路径

**解决方案**:
```bash
# 1. 清理可能的缓存
rm -rf .venv/.claude/cache

# 2. 重新运行修复脚本
./fix_venv_paths.sh

# 3. 使用启动脚本
./run.sh --version
```

---

## 📚 技术细节

### 动态路径检测机制

#### Bash/Zsh (activate)
```bash
VIRTUAL_ENV="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
```

#### Fish Shell (activate.fish)
```fish
set -gx VIRTUAL_ENV (cd (dirname (status -f))/..; and pwd)
```

#### C Shell (activate.csh)
```csh
setenv VIRTUAL_ENV `cd \`dirname $0\`/..; pwd`
```

#### PowerShell (Activate.ps1)
```powershell
$env:VIRTUAL_ENV=(Get-Item (Split-Path -Parent $PSCommandPath)).Parent.FullName
```

#### Python Shebang
```python
#!/usr/bin/env python
```

### 启动脚本工作流程

```
1. 检测项目根目录
   ↓
2. 验证虚拟环境存在
   ↓
3. 设置环境变量
   - VIRTUAL_ENV
   - CLAUDE_CONFIG_DIR
   - NPM_CONFIG_PREFIX
   - PATH
   ↓
4. 创建必要的目录
   ↓
5. 启动 Claude Code
```

---

## 🎓 最佳实践

### ✅ 推荐做法

1. **始终使用启动脚本**
   ```bash
   ./run.sh  # 而不是直接 claude
   ```

2. **版本控制**
   - ✅ 提交 `requirements.txt`
   - ✅ 提交启动脚本
   - ❌ 不提交 `.venv/` 目录

3. **文档同步**
   - 修改环境配置后更新相关文档
   - 保持 README.md 和本文档一致

4. **定期验证**
   ```bash
   # 定期检查绝对路径
   ./fix_venv_paths.sh
   ```

### ❌ 避免的做法

1. **不要直接修改 .venv 中的文件**
   - 使用 `fix_venv_paths.sh` 脚本

2. **不要硬编码路径**
   - 使用环境变量或相对路径

3. **不要跳过启动脚本**
   - 直接运行可能导致环境变量缺失

---

## 📊 可移植性检查清单

在分发项目前，确认以下项目：

- [ ] 运行 `./fix_venv_paths.sh` 修复绝对路径
- [ ] 验证 `./run.sh --version` 正常工作
- [ ] 检查 `.gitignore` 正确配置
- [ ] 更新 `requirements.txt`
- [ ] 测试在不同目录下运行
- [ ] 清理临时文件和缓存
- [ ] 更新文档中的路径示例

---

## 🔗 相关文档

- [README.md](README.md) - 项目概述和快速开始
- [VENV_ABSOLUTE_PATHS_REPORT.md](VENV_ABSOLUTE_PATHS_REPORT.md) - 绝对路径检查报告
- [VIRTUAL_ENV_PATH_EXPLANATION.md](VIRTUAL_ENV_PATH_EXPLANATION.md) - 虚拟环境路径说明
- [PORTABLE_SETUP.md](PORTABLE_SETUP.md) - 可移植性设置指南
- [CLAUDE_ENV_SETUP.md](CLAUDE_ENV_SETUP.md) - Claude 环境设置

---

## 📝 更新日志

### 2026-02-04
- ✅ 修复所有激活脚本中的绝对路径
- ✅ 修复 pip 等工具的 shebang
- ✅ 创建自动修复脚本 `fix_venv_paths.sh`
- ✅ 验证可移植性
- ✅ 创建本文档

---

**维护者**: Cline AI Assistant  
**项目**: aigc-film-agent  
**许可**: 遵循项目主许可证
