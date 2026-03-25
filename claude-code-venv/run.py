#!/usr/bin/env python3
"""
Claude Code 虚拟环境启动脚本 (Python)

这个脚本会：
1. 激活虚拟环境
2. 设置独立的用户目录
3. 启动 Claude Code
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def get_platform_info() -> tuple:
    """
    根据操作系统返回平台信息
    返回: (venv_name, bin_subdir, path_separator, is_windows)
    """
    system = platform.system()
    if system == "Windows":
        return "venv_win", "Scripts", ";", True
    elif system == "Linux":
        return "venv_linux", "bin", ":", False
    else:
        return "venv_mac", "bin", ":", False

def prepend_venv_to_path(env: dict, venv_path: Path, venv_bin_dir: Path, is_windows: bool) -> None:
    """
    将虚拟环境相关路径加入 PATH 最前面
    """
    if is_windows:
        path_entries = [str(venv_path), str(venv_bin_dir)]
        path_separator = ";"
    else:
        path_entries = [str(venv_bin_dir)]
        path_separator = ":"

    current_path = env.get("PATH", "")
    env["PATH"] = path_separator.join(path_entries + ([current_path] if current_path else []))

def get_portable_npm_paths(script_dir: Path) -> tuple[Path, Path]:
    """
    返回项目内专用的 npm 配置文件和缓存目录，避免读写用户全局配置
    """
    return script_dir / ".npmrc.portable", script_dir / ".npm-cache"

def prepare_portable_npm_env(env: dict, script_dir: Path, venv_path: Path) -> None:
    """
    配置仅对当前进程生效的 npm 环境，避免修改用户电脑的全局 npm 配置
    """
    npm_userconfig, npm_cache_dir = get_portable_npm_paths(script_dir)
    npm_cache_dir.mkdir(parents=True, exist_ok=True)
    npm_userconfig.touch(exist_ok=True)

    env["NPM_CONFIG_PREFIX"] = str(venv_path)
    env["NPM_CONFIG_USERCONFIG"] = str(npm_userconfig)
    env["NPM_CONFIG_CACHE"] = str(npm_cache_dir)
    env["NPM_CONFIG_UPDATE_NOTIFIER"] = "false"
    env["NPM_CONFIG_FUND"] = "false"
    env["NPM_CONFIG_AUDIT"] = "false"

def get_claude_executable(venv_path: Path, bin_dir: Path, is_windows: bool) -> Path:
    """
    查找 Claude 可执行文件
    """
    if is_windows:
        # Windows 上 npm 全局安装会创建多个文件，按优先级查找
        # npm 使用 prefix 时，可执行文件可能在 prefix 根目录或 Scripts 目录
        search_dirs = [venv_path, bin_dir]  # 先查根目录，再查 Scripts
        for search_dir in search_dirs:
            for name in ["claude.cmd", "claude.ps1", "claude"]:
                candidate = search_dir / name
                if candidate.exists():
                    return candidate
        # 如果都不存在，默认使用根目录的 claude.cmd（用于错误提示）
        return venv_path / "claude.cmd"
    else:
        return bin_dir / "claude"

def main():
    # 获取脚本所在目录（虚拟环境目录）
    script_dir = Path(__file__).parent.absolute()
    
    # 根据平台选择虚拟环境目录
    venv_name, bin_subdir, path_separator, is_windows = get_platform_info()
    venv_path = script_dir / venv_name
    
    # 获取终端当前工作目录（用户执行脚本时所在的目录）
    current_dir = Path.cwd().absolute()
    
    # 获取平台相关路径
    venv_bin_dir = venv_path / bin_subdir
    claude_bin = get_claude_executable(venv_path, venv_bin_dir, is_windows)
    
    # 检查虚拟环境是否存在
    if not venv_path.exists():
        print("❌ 错误：虚拟环境不存在")
        print(f"📍 期望路径: {venv_path}")
        print("\n💡 请先创建虚拟环境：")
        if is_windows:
            print("   python build_venv.py --win")
        else:
            print("   python3 build_venv.py")
        sys.exit(1)
    
    # 检查 Claude Code 是否已安装
    if not claude_bin.exists():
        print("❌ 错误：Claude Code 未安装在虚拟环境中")
        print(f"📍 期望路径: {claude_bin}")
        print("\n💡 请先安装 Claude Code：")
        if is_windows:
            print(f"   call {venv_name}\\Scripts\\activate_claude.bat")
            print("   npm install -g @anthropic-ai/claude-code")
        else:
            print(f"   source {venv_name}/bin/activate_claude")
            print("   npm install -g @anthropic-ai/claude-code")
        sys.exit(1)
    
    # 设置环境变量
    env = os.environ.copy()
    
    # 设置虚拟环境路径
    env["VIRTUAL_ENV"] = str(venv_path)

    # 设置仅对当前进程生效的 npm 环境（不写用户全局配置）
    prepare_portable_npm_env(env, script_dir, venv_path)
    
    # 🔑 从 .env 文件读取环境变量（优先级最高）
    env_file = script_dir / ".env"
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过注释和空行
                    if line and not line.startswith('#'):
                        # 解析 KEY=VALUE 格式
                        if '=' in line:
                            key, value = line.split('=', 1)
                            env[key.strip()] = value.strip()
        except Exception as e:
            print(f"Warning: Failed to load .env file: {e}", file=sys.stderr)
    
    # 设置独立的 Claude 用户目录
    # 如果 .env 中设置了 CLAUDE_CONFIG_DIR，判断是相对还是绝对路径
    if "CLAUDE_CONFIG_DIR" in env:
        config_dir_path = Path(env["CLAUDE_CONFIG_DIR"])
        if not config_dir_path.is_absolute():
            # 相对路径，相对于脚本目录
            config_dir_path = script_dir / config_dir_path
        env["CLAUDE_CONFIG_DIR"] = str(config_dir_path.absolute())
    else:
        # 默认值：claude-code-venv/.claude
        claude_config_dir = script_dir / ".claude"
        env["CLAUDE_CONFIG_DIR"] = str(claude_config_dir)
    
    # 🔑 从 settings.json 读取并导出 API 配置环境变量（作为备用）
    settings_file = Path(env["CLAUDE_CONFIG_DIR"]) / "settings.json"
    if settings_file.exists():
        try:
            import json
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                env_vars = settings.get('env', {})
                for key, value in env_vars.items():
                    # 如果 .env 中已经设置，则不覆盖
                    if key not in env or not env[key]:
                        env[key] = value
        except Exception as e:
            print(f"Warning: Failed to load settings.json: {e}", file=sys.stderr)
    
    # 更新 PATH，将虚拟环境路径放在最前面
    prepend_venv_to_path(env, venv_path, venv_bin_dir, is_windows)
    
    # 创建独立的配置目录
    Path(env["CLAUDE_CONFIG_DIR"]).mkdir(parents=True, exist_ok=True)
    
    # 读取版本号
    version_file = script_dir / "VERSION"
    version = "unknown"
    if version_file.exists():
        version = version_file.read_text(encoding='utf-8').strip()
    
    # 打印启动信息
    print("=" * 60)
    print(f"🚀 启动 Claude Code 虚拟环境 v{version}")
    print("=" * 60)
    print(f"📂 终端目录: {current_dir}")
    print(f"📍 脚本目录: {script_dir}")
    print(f"📦 虚拟环境: {venv_path}")
    print(f"🗂️  用户目录: {env['CLAUDE_CONFIG_DIR']}")
    print(f"🔧 Claude 路径: {claude_bin}")
    print("=" * 60)
    print()
    
    # 启动 Claude Code
    try:
        # 传递命令行参数给 Claude Code
        claude_args = sys.argv[1:] if len(sys.argv) > 1 else []
        
        # 执行 Claude Code（工作目录为终端当前目录）
        result = subprocess.run(
            [str(claude_bin)] + claude_args,
            env=env,
            cwd=str(current_dir)
        )
        
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n\n👋 Claude Code 已退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
