#!/usr/bin/env python3
"""
Claude Code 虚拟环境构建脚本

功能：
- 自动检测操作系统
- 创建 Python 虚拟环境（venv_mac、venv_linux、venv_win）
- 安装 nodeenv 并嵌入 Node.js 环境
- 通过 npm 安装 Claude Code
- 支持选择性构建或全部构建

使用方法：
    python3 build_venv.py              # 只构建当前系统的虚拟环境
    python3 build_venv.py --all        # 构建所有系统的虚拟环境
    python3 build_venv.py --mac        # 只构建 macOS 虚拟环境
    python3 build_venv.py --linux      # 只构建 Linux 虚拟环境
    python3 build_venv.py --win        # 只构建 Windows 虚拟环境
    python3 build_venv.py --node-version 20.11.0  # 指定 Node.js 版本
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
from pathlib import Path


class VenvBuilder:
    """虚拟环境构建器"""
    
    def __init__(self, script_dir, node_version='20.11.0'):
        self.script_dir = Path(script_dir)
        self.system = platform.system().lower()
        self.node_version = node_version
        
        # 虚拟环境配置
        self.venv_configs = {
            'mac': {
                'name': 'venv_mac',
                'platform': 'darwin',
                'python_cmd': 'python3',
                'pip_cmd': 'pip3',
                'bin_dir': 'bin',
                'activate': 'bin/activate',
                'node_modules': 'lib/node_modules'
            },
            'linux': {
                'name': 'venv_linux',
                'platform': 'linux',
                'python_cmd': 'python3',
                'pip_cmd': 'pip3',
                'bin_dir': 'bin',
                'activate': 'bin/activate',
                'node_modules': 'lib/node_modules'
            },
            'win': {
                'name': 'venv_win',
                'platform': 'windows',
                'python_cmd': 'python',
                'pip_cmd': 'pip',
                'bin_dir': 'Scripts',
                'activate': 'Scripts\\activate.bat',
                'node_modules': 'Lib\\node_modules'
            }
        }
    
    def get_current_platform(self):
        """获取当前平台标识"""
        if self.system == 'darwin':
            return 'mac'
        elif self.system == 'linux':
            return 'linux'
        elif self.system == 'windows':
            return 'win'
        else:
            return None

    def get_claude_executable(self, platform_key):
        """获取 Claude 可执行文件路径"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']

        if platform_key == 'win':
            # Windows 下 npm 使用 prefix 全局安装时，启动文件通常位于 prefix 根目录，
            # 而不是 Python venv 的 Scripts 目录。
            search_dirs = [venv_path, venv_path / 'Scripts']
            for search_dir in search_dirs:
                for name in ['claude.cmd', 'claude.ps1', 'claude', 'claude.exe']:
                    candidate = search_dir / name
                    if candidate.exists():
                        return candidate
            return venv_path / 'claude.cmd'

        return venv_path / 'bin' / 'claude'

    def build_runtime_env(self, platform_key):
        """构建用于验证/运行的环境变量"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        env = os.environ.copy()
        env['VIRTUAL_ENV'] = str(venv_path)
        self.prepare_portable_npm_env(env, venv_path)

        if platform_key == 'win':
            path_entries = [str(venv_path), str(venv_path / config['bin_dir'])]
            path_separator = ';'
        else:
            path_entries = [str(venv_path / config['bin_dir'])]
            path_separator = ':'

        current_path = env.get('PATH', '')
        env['PATH'] = path_separator.join(path_entries + ([current_path] if current_path else []))
        return env

    def get_portable_npm_paths(self):
        """返回项目内专用 npm 配置路径，避免读写用户全局配置"""
        return self.script_dir / '.npmrc.portable', self.script_dir / '.npm-cache'

    def prepare_portable_npm_env(self, env, venv_path):
        """配置仅对当前进程生效的 npm 环境变量"""
        npm_userconfig, npm_cache_dir = self.get_portable_npm_paths()
        npm_cache_dir.mkdir(parents=True, exist_ok=True)
        npm_userconfig.touch(exist_ok=True)

        env['NPM_CONFIG_PREFIX'] = str(venv_path)
        env['NPM_CONFIG_USERCONFIG'] = str(npm_userconfig)
        env['NPM_CONFIG_CACHE'] = str(npm_cache_dir)
        env['NPM_CONFIG_UPDATE_NOTIFIER'] = 'false'
        env['NPM_CONFIG_FUND'] = 'false'
        env['NPM_CONFIG_AUDIT'] = 'false'
        return env
    
    def print_header(self, text):
        """打印标题"""
        print("\n" + "=" * 60)
        print(f"🔧 {text}")
        print("=" * 60)
    
    def print_info(self, text):
        """打印信息"""
        print(f"ℹ️  {text}")
    
    def print_success(self, text):
        """打印成功信息"""
        print(f"✅ {text}")
    
    def print_error(self, text):
        """打印错误信息"""
        print(f"❌ {text}")
    
    def print_warning(self, text):
        """打印警告信息"""
        print(f"⚠️  {text}")
    
    def check_python_version(self):
        """检查 Python 版本"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_error(f"需要 Python 3.8 或更高版本，当前版本：{version.major}.{version.minor}")
            return False
        self.print_success(f"Python 版本检查通过：{version.major}.{version.minor}.{version.micro}")
        return True
    
    def create_venv(self, platform_key):
        """创建 Python 虚拟环境"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        
        self.print_header(f"步骤 1/4: 创建 Python 虚拟环境")
        
        # 检查是否已存在
        if venv_path.exists():
            self.print_warning(f"虚拟环境已存在：{venv_path}")
            response = input("是否删除并重新创建？(y/N): ").strip().lower()
            if response == 'y':
                self.print_info(f"删除现有虚拟环境：{venv_path}")
                shutil.rmtree(venv_path)
            else:
                self.print_info("跳过创建，使用现有虚拟环境")
                return True
        
        # 创建虚拟环境
        self.print_info(f"创建 Python 虚拟环境：{venv_path}")
        try:
            subprocess.run(
                [config['python_cmd'], '-m', 'venv', str(venv_path)],
                check=True,
                capture_output=True,
                text=True
            )
            self.print_success(f"Python 虚拟环境创建成功")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"创建虚拟环境失败：{e}")
            if e.stderr:
                print(e.stderr)
            return False
        except FileNotFoundError:
            self.print_error(f"未找到 Python 命令：{config['python_cmd']}")
            self.print_info("请确保已安装 Python 并添加到 PATH")
            return False
    
    def install_nodeenv(self, platform_key):
        """安装 nodeenv"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        
        self.print_header(f"步骤 2/4: 安装 nodeenv")
        
        if not venv_path.exists():
            self.print_error(f"虚拟环境不存在：{venv_path}")
            return False
        
        # 确定 pip 路径
        if platform_key == 'win':
            pip_path = venv_path / 'Scripts' / 'pip.exe'
        else:
            pip_path = venv_path / 'bin' / 'pip'
        
        if not pip_path.exists():
            self.print_error(f"未找到 pip：{pip_path}")
            return False
        
        # 升级 pip
        self.print_info("升级 pip...")
        try:
            subprocess.run(
                [str(pip_path), 'install', '--upgrade', 'pip'],
                check=True,
                capture_output=True,
                text=True
            )
            self.print_success("pip 升级成功")
        except subprocess.CalledProcessError as e:
            self.print_warning(f"pip 升级失败（可能不影响后续安装）")
        
        # 安装 nodeenv
        self.print_info("安装 nodeenv...")
        try:
            subprocess.run(
                [str(pip_path), 'install', 'nodeenv'],
                check=True,
                capture_output=True,
                text=True
            )
            self.print_success("nodeenv 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"nodeenv 安装失败：{e}")
            if e.stderr:
                print(e.stderr)
            return False
    
    def setup_nodejs(self, platform_key):
        """使用 nodeenv 设置 Node.js 环境"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        
        self.print_header(f"步骤 3/4: 设置 Node.js 环境")
        
        # 确定 nodeenv 路径
        if platform_key == 'win':
            nodeenv_path = venv_path / 'Scripts' / 'nodeenv.exe'
        else:
            nodeenv_path = venv_path / 'bin' / 'nodeenv'
        
        if not nodeenv_path.exists():
            self.print_error(f"未找到 nodeenv：{nodeenv_path}")
            return False
        
        # 使用 nodeenv 在虚拟环境中安装 Node.js
        self.print_info(f"安装 Node.js {self.node_version}（这可能需要几分钟）...")
        self.print_info("正在从 nodejs.org 下载 Node.js...")
        
        # 尝试多次安装（处理网络问题）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # nodeenv 会将 Node.js 安装到虚拟环境中
                # 使用 --force 参数覆盖已存在的环境
                result = subprocess.run(
                    [str(nodeenv_path), '--node', self.node_version, '--prebuilt', '--force', str(venv_path)],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=600  # 10分钟超时
                )
                self.print_success(f"Node.js {self.node_version} 安装成功")
                break  # 成功则跳出循环
            except subprocess.CalledProcessError as e:
                if attempt < max_retries - 1:
                    self.print_warning(f"安装失败（尝试 {attempt + 1}/{max_retries}），正在重试...")
                    import time
                    time.sleep(2)  # 等待2秒后重试
                    continue
                else:
                    # 最后一次尝试失败
                    self.print_error(f"Node.js 安装失败（已重试 {max_retries} 次）")
                    if e.stderr:
                        # 检查是否是网络问题
                        if 'SSL' in e.stderr or 'urlopen' in e.stderr or 'URLError' in e.stderr:
                            self.print_error("检测到网络/SSL 错误")
                            self.print_info("可能的解决方案：")
                            self.print_info("1. 检查网络连接")
                            self.print_info("2. 配置代理：export HTTP_PROXY=http://127.0.0.1:7890")
                            self.print_info("3. 尝试使用不同的 Node.js 版本")
                            self.print_info("4. 手动下载 Node.js 并使用本地安装")
                        print("\n错误详情：")
                        print(e.stderr[:500])  # 只显示前500字符
                    return False
            except subprocess.TimeoutExpired:
                self.print_error("Node.js 安装超时（可能网络较慢）")
                return False
        
        # 验证安装成功后继续
        try:
            
            # 验证 Node.js 安装
            if platform_key == 'win':
                node_path = venv_path / 'Scripts' / 'node.exe'
                npm_path = venv_path / 'Scripts' / 'npm.cmd'
            else:
                node_path = venv_path / 'bin' / 'node'
                npm_path = venv_path / 'bin' / 'npm'
            
            if node_path.exists() and npm_path.exists():
                # 获取 Node.js 版本
                result = subprocess.run(
                    [str(node_path), '--version'],
                    capture_output=True,
                    text=True
                )
                node_ver = result.stdout.strip()
                
                # 获取 npm 版本
                result = subprocess.run(
                    [str(npm_path), '--version'],
                    capture_output=True,
                    text=True
                )
                npm_ver = result.stdout.strip()
                
                self.print_success(f"Node.js 版本：{node_ver}")
                self.print_success(f"npm 版本：{npm_ver}")
                return True
            else:
                self.print_error("Node.js 或 npm 未正确安装")
                return False
                
        except subprocess.CalledProcessError as e:
            self.print_error(f"Node.js 安装失败：{e}")
            if e.stderr:
                print(e.stderr)
            return False
        except subprocess.TimeoutExpired:
            self.print_error("Node.js 安装超时（可能网络较慢）")
            return False
    
    def install_claude_code(self, platform_key):
        """通过 npm 安装 Claude Code"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        env = self.build_runtime_env(platform_key)
        
        self.print_header(f"步骤 4/4: 安装 Claude Code")
        
        if not venv_path.exists():
            self.print_error(f"虚拟环境不存在：{venv_path}")
            return False
        
        # 确定 npm 路径
        if platform_key == 'win':
            npm_path = venv_path / 'Scripts' / 'npm.cmd'
        else:
            npm_path = venv_path / 'bin' / 'npm'
        
        if not npm_path.exists():
            self.print_error(f"未找到 npm：{npm_path}")
            return False
        
        self.print_info("使用项目内临时 npm 环境安装（不会修改用户全局 npm 配置）...")
        
        # 安装 Claude Code
        self.print_info("安装 @anthropic-ai/claude-code（这可能需要几分钟）...")
        try:
            result = subprocess.run(
                [str(npm_path), 'install', '-g', '@anthropic-ai/claude-code'],
                check=True,
                capture_output=True,
                text=True,
                timeout=600,  # 10分钟超时
                env=env
            )
            self.print_success("Claude Code 安装成功")
            
            # 验证安装
            return self.verify_installation(platform_key)
        except subprocess.CalledProcessError as e:
            self.print_error(f"Claude Code 安装失败：{e}")
            if e.stderr:
                print(e.stderr)
            return False
        except subprocess.TimeoutExpired:
            self.print_error("Claude Code 安装超时（可能网络较慢）")
            return False
    
    def verify_installation(self, platform_key):
        """验证安装"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        env = self.build_runtime_env(platform_key)

        claude_path = self.get_claude_executable(platform_key)
        
        if not claude_path.exists():
            self.print_error(f"未找到 claude 命令：{claude_path}")
            return False
        
        self.print_info("验证 Claude Code 安装...")
        try:
            result = subprocess.run(
                [str(claude_path), '--version'],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )
            version = result.stdout.strip()
            self.print_success(f"Claude Code 版本：{version}")
            
            # 检查 node_modules
            node_modules_path = venv_path / config['node_modules']
            if node_modules_path.exists():
                self.print_success(f"node_modules 位置：{node_modules_path}")
            
            return True
        except subprocess.CalledProcessError as e:
            self.print_error(f"验证失败：{e}")
            return False
        except subprocess.TimeoutExpired:
            self.print_error("验证超时")
            return False
    
    def fix_absolute_paths(self, platform_key):
        """修复虚拟环境中的绝对路径，使其可移植"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        
        self.print_info("修复绝对路径以提高可移植性...")
        
        fixed_count = 0
        
        # 修复 activate 脚本
        if platform_key == 'win':
            # Windows 的 activate 脚本
            activate_files = [
                venv_path / 'Scripts' / 'activate.bat',
                venv_path / 'Scripts' / 'Activate.ps1'
            ]
        else:
            # Unix 的 activate 脚本
            activate_files = [
                venv_path / 'bin' / 'activate',
                venv_path / 'bin' / 'activate.fish',
                venv_path / 'bin' / 'activate.csh'
            ]
        
        for activate_file in activate_files:
            if activate_file.exists():
                try:
                    content = activate_file.read_text()
                    # 将绝对路径替换为相对路径检测
                    if platform_key == 'win':
                        # Windows PowerShell
                        if 'Activate.ps1' in str(activate_file):
                            content = content.replace(
                                f'$env:VIRTUAL_ENV="{venv_path}"',
                                '$env:VIRTUAL_ENV=(Get-Item (Split-Path -Parent $PSCommandPath)).Parent.FullName'
                            )
                    else:
                        # Unix shells
                        content = content.replace(
                            f'VIRTUAL_ENV="{venv_path}"',
                            'VIRTUAL_ENV="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"'
                        )
                        content = content.replace(
                            f'set -gx VIRTUAL_ENV "{venv_path}"',
                            'set -gx VIRTUAL_ENV (cd (dirname (status -f))/..; and pwd)'
                        )
                        content = content.replace(
                            f'setenv VIRTUAL_ENV "{venv_path}"',
                            'setenv VIRTUAL_ENV `cd `dirname $0`/..; pwd`'
                        )
                    
                    activate_file.write_text(content)
                    fixed_count += 1
                except Exception as e:
                    self.print_warning(f"修复 {activate_file.name} 失败：{e}")
        
        # 修复可执行文件的 shebang
        if platform_key != 'win':
            bin_dir = venv_path / 'bin'
            for file in bin_dir.iterdir():
                if file.is_file() and not file.is_symlink():
                    try:
                        # 读取第一行
                        with open(file, 'rb') as f:
                            first_line = f.readline()
                        
                        # 检查是否是 shebang 且包含绝对路径
                        if first_line.startswith(b'#!') and str(venv_path).encode() in first_line:
                            # 读取整个文件
                            content = file.read_bytes()
                            # 替换 shebang 为 /usr/bin/env python
                            new_content = content.replace(
                                f'#!{venv_path}/bin/python'.encode(),
                                b'#!/usr/bin/env python'
                            )
                            if new_content != content:
                                file.write_bytes(new_content)
                                fixed_count += 1
                    except Exception:
                        # 忽略二进制文件或无法读取的文件
                        pass
        
        if fixed_count > 0:
            self.print_success(f"已修复 {fixed_count} 个文件的绝对路径")
        else:
            self.print_info("未发现需要修复的绝对路径")
        
        return True
    
    def create_activate_claude_script(self, platform_key):
        """创建 activate_claude 便捷脚本（使用相对路径）"""
        config = self.venv_configs[platform_key]
        venv_path = self.script_dir / config['name']
        
        if platform_key == 'win':
            # Windows 批处理脚本
            script_path = venv_path / 'Scripts' / 'activate_claude.bat'
            content = r"""@echo off
REM Claude Code 虚拟环境激活脚本

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
set VENV_DIR=%SCRIPT_DIR%..

REM 激活虚拟环境
call "%SCRIPT_DIR%activate.bat"

REM 设置 npm 全局路径
set NPM_CONFIG_PREFIX=%VENV_DIR%
set NPM_CONFIG_USERCONFIG=%VENV_DIR%\..\.npmrc.portable
set NPM_CONFIG_CACHE=%VENV_DIR%\..\.npm-cache
set NPM_CONFIG_UPDATE_NOTIFIER=false
set NPM_CONFIG_FUND=false
set NPM_CONFIG_AUDIT=false

REM npm 在 Windows + prefix 模式下通常把 claude.cmd 放在虚拟环境根目录
set PATH=%VENV_DIR%;%PATH%

echo.
echo ============================================================
echo Claude Code 虚拟环境已激活
echo ============================================================
echo Python: %VIRTUAL_ENV%
echo Node.js: %SCRIPT_DIR%node.exe
echo Claude: %VENV_DIR%\claude.cmd
echo ============================================================
"""
        else:
            # Unix shell 脚本（使用相对路径）
            script_path = venv_path / 'bin' / 'activate_claude'
            content = """#!/bin/bash
# Claude Code 虚拟环境激活脚本

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$(dirname "$SCRIPT_DIR")"

# 激活 Python 虚拟环境
source "$SCRIPT_DIR/activate"

# 设置 npm 全局路径
export NPM_CONFIG_PREFIX="$VENV_DIR"
export NPM_CONFIG_USERCONFIG="$VENV_DIR/../.npmrc.portable"
export NPM_CONFIG_CACHE="$VENV_DIR/../.npm-cache"
export NPM_CONFIG_UPDATE_NOTIFIER="false"
export NPM_CONFIG_FUND="false"
export NPM_CONFIG_AUDIT="false"

# 确保 PATH 优先级
export PATH="$SCRIPT_DIR:$PATH"

echo ""
echo "============================================================"
echo "Claude Code 虚拟环境已激活"
echo "============================================================"
echo "Python: $VIRTUAL_ENV"
echo "Node.js: $SCRIPT_DIR/node"
echo "Claude: $SCRIPT_DIR/claude"
echo "============================================================"
echo ""
"""
        
        try:
            script_path.write_text(content)
            if platform_key != 'win':
                script_path.chmod(0o755)
            self.print_success(f"创建激活脚本：{script_path.name}")
            return True
        except Exception as e:
            self.print_warning(f"创建激活脚本失败：{e}")
            return False

    def create_entry_scripts(self):
        """创建根目录入口脚本（无需系统 Python）"""
        scripts = {
            'run.bat': r"""@echo off
setlocal

REM Claude Code 便携启动入口（无需系统 Python）
set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=%SCRIPT_DIR%venv_win\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo ❌ 未找到 Windows 虚拟环境：%PYTHON_EXE%
    echo.
    echo 请先在当前目录构建 Windows 虚拟环境：
    echo    python build_venv.py --win
    exit /b 1
)

"%PYTHON_EXE%" "%SCRIPT_DIR%run.py" %*
exit /b %ERRORLEVEL%
""",
            'run.sh': """#!/bin/sh

# Claude Code 便携启动入口（无需系统 Python）

SCRIPT_DIR=\"$(CDPATH= cd -- \"$(dirname \"$0\")\" && pwd)\"
SYSTEM_NAME=\"$(uname -s)\"

case \"$SYSTEM_NAME\" in
    Darwin*)
        PYTHON_EXE=\"$SCRIPT_DIR/venv_mac/bin/python\"
        ;;
    Linux*)
        PYTHON_EXE=\"$SCRIPT_DIR/venv_linux/bin/python\"
        ;;
    *)
        echo \"❌ 不支持的系统：$SYSTEM_NAME\"
        exit 1
        ;;
esac

if [ ! -x \"$PYTHON_EXE\" ]; then
    echo \"❌ 未找到对应虚拟环境：$PYTHON_EXE\"
    echo
    echo \"请先在当前目录构建当前系统的虚拟环境：\"
    echo \"   python3 build_venv.py\"
    exit 1
fi

exec \"$PYTHON_EXE\" \"$SCRIPT_DIR/run.py\" \"$@\"
"""
        }

        created = []
        for file_name, content in scripts.items():
            script_path = self.script_dir / file_name
            try:
                script_path.write_text(content, encoding='utf-8')
                if file_name.endswith('.sh'):
                    script_path.chmod(0o755)
                created.append(file_name)
            except Exception as e:
                self.print_warning(f"创建入口脚本 {file_name} 失败：{e}")

        if created:
            self.print_success(f"创建入口脚本：{', '.join(created)}")
        return True
    
    def build(self, platform_key):
        """构建指定平台的虚拟环境"""
        config = self.venv_configs[platform_key]
        
        self.print_header(f"开始构建 {config['name']}")
        self.print_info(f"目标平台：{config['platform']}")
        self.print_info(f"Node.js 版本：{self.node_version}")
        self.print_info(f"虚拟环境目录：{self.script_dir / config['name']}")
        
        # 步骤 1: 创建 Python 虚拟环境
        if not self.create_venv(platform_key):
            return False
        
        # 步骤 2: 安装 nodeenv
        if not self.install_nodeenv(platform_key):
            return False
        
        # 步骤 3: 设置 Node.js 环境
        if not self.setup_nodejs(platform_key):
            return False
        
        # 步骤 4: 安装 Claude Code
        if not self.install_claude_code(platform_key):
            return False
        
        # 步骤 5: 修复绝对路径（提高可移植性）
        self.print_header(f"步骤 5/5: 修复绝对路径")
        self.fix_absolute_paths(platform_key)
        
        # 创建便捷激活脚本
        self.create_activate_claude_script(platform_key)
        self.create_entry_scripts()
        
        self.print_success(f"{config['name']} 构建完成！")
        return True
    
    def build_all(self, platforms):
        """构建多个平台的虚拟环境"""
        self.print_header("批量构建虚拟环境")
        self.print_info(f"将构建以下平台：{', '.join(platforms)}")
        
        results = {}
        for platform_key in platforms:
            success = self.build(platform_key)
            results[platform_key] = success
        
        # 显示总结
        self.print_header("构建总结")
        for platform_key, success in results.items():
            config = self.venv_configs[platform_key]
            if success:
                self.print_success(f"{config['name']}: 构建成功")
            else:
                self.print_error(f"{config['name']}: 构建失败")
        
        # 返回是否全部成功
        return all(results.values())


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Claude Code 虚拟环境构建脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 build_venv.py                    # 只构建当前系统的虚拟环境
  python3 build_venv.py --all              # 构建所有系统的虚拟环境
  python3 build_venv.py --mac              # 只构建 macOS 虚拟环境
  python3 build_venv.py --linux            # 只构建 Linux 虚拟环境
  python3 build_venv.py --win              # 只构建 Windows 虚拟环境
  python3 build_venv.py --mac --linux      # 构建 macOS 和 Linux 虚拟环境
  python3 build_venv.py --node-version 18.19.0  # 指定 Node.js 版本
        """
    )
    
    parser.add_argument('--all', action='store_true', help='构建所有平台的虚拟环境')
    parser.add_argument('--mac', action='store_true', help='构建 macOS 虚拟环境')
    parser.add_argument('--linux', action='store_true', help='构建 Linux 虚拟环境')
    parser.add_argument('--win', action='store_true', help='构建 Windows 虚拟环境')
    parser.add_argument('--node-version', default='20.11.0', help='Node.js 版本（默认：20.11.0）')
    
    args = parser.parse_args()
    
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    
    # 创建构建器
    builder = VenvBuilder(script_dir, node_version=args.node_version)
    
    # 检查 Python 版本
    if not builder.check_python_version():
        sys.exit(1)
    
    # 确定要构建的平台
    platforms = []
    
    if args.all:
        platforms = ['mac', 'linux', 'win']
    else:
        if args.mac:
            platforms.append('mac')
        if args.linux:
            platforms.append('linux')
        if args.win:
            platforms.append('win')
        
        # 如果没有指定任何平台，则构建当前平台
        if not platforms:
            current_platform = builder.get_current_platform()
            if current_platform:
                platforms.append(current_platform)
                builder.print_info(f"未指定平台，将构建当前平台：{current_platform}")
            else:
                builder.print_error(f"不支持的操作系统：{builder.system}")
                sys.exit(1)
    
    # 显示欢迎信息
    print("\n" + "=" * 60)
    print("🚀 Claude Code 虚拟环境构建脚本")
    print("=" * 60)
    print(f"📂 工作目录：{script_dir}")
    print(f"🖥️  当前系统：{builder.system}")
    print(f"🎯 构建目标：{', '.join(platforms)}")
    print(f"📦 Node.js 版本：{args.node_version}")
    print("=" * 60)
    print("\n构建流程：")
    print("  1️⃣  创建 Python 虚拟环境")
    print("  2️⃣  安装 nodeenv")
    print("  3️⃣  设置 Node.js 环境")
    print("  4️⃣  安装 Claude Code")
    print()
    
    # 执行构建
    if len(platforms) == 1:
        success = builder.build(platforms[0])
    else:
        success = builder.build_all(platforms)
    
    # 退出
    if success:
        print("\n" + "=" * 60)
        print("🎉 所有虚拟环境构建完成！")
        print("=" * 60)
        print("\n下一步：")
        print("1. 配置环境变量：cp .env.example .env")
        print("2. 编辑 .env 文件，填入你的 API 密钥")
        print("3. 启动 Claude Code：Windows 用 run.bat，macOS/Linux 用 ./run.sh")
        print("\n或者使用便捷激活脚本：")
        for platform in platforms:
            config = builder.venv_configs[platform]
            if platform == 'win':
                print(f"   Windows: {config['name']}\\Scripts\\activate_claude.bat")
            else:
                print(f"   {platform}: source {config['name']}/bin/activate_claude")
        print()
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ 部分虚拟环境构建失败")
        print("=" * 60)
        print("\n请检查错误信息并重试")
        print()
        sys.exit(1)


if __name__ == '__main__':
    main()
