#!/usr/bin/env python3
"""
Claude Code 虚拟环境升级脚本

这个脚本会：
1. 检测操作系统和虚拟环境
2. 让用户选择要升级的虚拟环境
3. 检查当前安装的 Claude Code 版本
4. 升级到最新版本
5. 显示升级结果
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
from typing import List, Tuple

def get_platform_info() -> tuple:
    """
    根据操作系统返回平台信息
    返回: (venv_name, bin_subdir, is_windows)
    """
    if platform.system() == "Windows":
        return "venv_win", "Scripts", True
    else:
        return "venv_mac", "bin", False

def get_available_venvs(script_dir: Path) -> List[Tuple[str, str, str]]:
    """
    获取可用的虚拟环境列表
    返回: [(venv_name, bin_subdir, display_name), ...]
    """
    venvs = []
    
    # 检查 macOS 虚拟环境
    if (script_dir / "venv_mac").exists():
        venvs.append(("venv_mac", "bin", "macOS"))
    
    # 检查 Windows 虚拟环境
    if (script_dir / "venv_win").exists():
        venvs.append(("venv_win", "Scripts", "Windows"))
    
    return venvs

def run_command(cmd: list, env: dict, cwd: Path = None, timeout: int = None, show_output: bool = False) -> tuple:
    """
    执行命令并返回结果
    返回: (returncode, stdout, stderr)
    """
    try:
        if show_output:
            # 实时显示输出
            process = subprocess.Popen(
                cmd,
                env=env,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            for line in process.stdout:
                print(line, end='', flush=True)
                output_lines.append(line)
            
            process.wait(timeout=timeout)
            return process.returncode, ''.join(output_lines), ''
        else:
            result = subprocess.run(
                cmd,
                env=env,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=timeout
            )
            return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "命令执行超时"
    except Exception as e:
        return -1, "", str(e)

def get_npm_package_version(package_name: str, env: dict) -> str:
    """
    获取已安装的 npm 包版本
    """
    returncode, stdout, stderr = run_command(
        ["npm", "list", "-g", package_name, "--json"],
        env,
        timeout=30
    )
    
    if returncode == 0 and stdout:
        try:
            data = json.loads(stdout)
            dependencies = data.get("dependencies", {})
            if package_name in dependencies:
                return dependencies[package_name].get("version", "unknown")
        except:
            pass
    
    return "未安装"

def upgrade_venv(script_dir: Path, venv_name: str, bin_subdir: str, display_name: str, package_name: str) -> bool:
    """
    升级指定的虚拟环境
    返回: 是否成功
    """
    venv_path = script_dir / venv_name
    venv_bin_dir = venv_path / bin_subdir
    is_windows = (venv_name == "venv_win")
    
    print()
    print("=" * 70)
    print(f"🔄 升级 {display_name} 虚拟环境")
    print("=" * 70)
    print(f"📦 虚拟环境: {venv_path}")
    print("=" * 70)
    print()
    
    # 设置环境变量
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(venv_path)
    env["NPM_CONFIG_PREFIX"] = str(venv_path)
    
    # 更新 PATH
    venv_bin = str(venv_bin_dir)
    if "PATH" in env:
        path_separator = ";" if is_windows else ":"
        env["PATH"] = f"{venv_bin}{path_separator}{env['PATH']}"
    else:
        env["PATH"] = venv_bin
    
    # 检查 npm 是否可用
    print("🔍 检查 npm 是否可用...")
    returncode, stdout, stderr = run_command(["npm", "--version"], env, timeout=10)
    
    if returncode != 0:
        print("❌ 错误：npm 不可用")
        print(f"错误信息: {stderr}")
        return False
    
    npm_version = stdout.strip()
    print(f"✅ npm 版本: {npm_version}")
    print()
    
    # 获取当前安装的 Claude Code 版本
    print(f"🔍 检查当前 {package_name} 版本...")
    current_version = get_npm_package_version(package_name, env)
    print(f"📦 当前版本: {current_version}")
    print()
    
    # 检查是否有可用更新
    print("🔍 检查是否有可用更新...")
    print("⏳ 正在连接 npm 仓库...")
    returncode, stdout, stderr = run_command(
        ["npm", "outdated", "-g", package_name, "--json"],
        env,
        timeout=60
    )
    
    has_update = False
    latest_version = "unknown"
    
    if stdout:
        try:
            data = json.loads(stdout)
            if package_name in data:
                latest_version = data[package_name].get("latest", "unknown")
                has_update = True
        except:
            pass
    
    if has_update:
        print(f"✨ 发现新版本: {latest_version}")
    else:
        print("✅ 已是最新版本")
    print()
    
    # 执行升级
    print("=" * 70)
    print("🚀 开始升级...")
    print("=" * 70)
    print()
    
    print(f"📦 正在升级 {package_name}...")
    print("⏳ 这可能需要几分钟时间，请耐心等待...")
    print("💡 提示：如果长时间无响应，可以按 Ctrl+C 中断")
    print()
    print("--- npm 输出 ---")
    
    # 使用实时输出模式，设置较长的超时时间（10分钟）
    returncode, stdout, stderr = run_command(
        ["npm", "install", "-g", package_name],
        env,
        timeout=600,
        show_output=True
    )
    
    print("--- npm 输出结束 ---")
    print()
    
    if returncode != 0:
        print("❌ 升级失败")
        if stderr:
            print(f"错误信息: {stderr}")
        print("\n💡 可能的原因：")
        print("   1. 网络连接问题")
        print("   2. npm 仓库访问受限")
        print("   3. 权限不足")
        print("\n💡 建议尝试：")
        print("   1. 检查网络连接")
        print("   2. 使用 VPN 或更换网络")
        print("   3. 手动执行升级命令")
        return False
    
    print("✅ 升级完成")
    print()
    
    # 获取升级后的版本
    print("🔍 验证升级结果...")
    new_version = get_npm_package_version(package_name, env)
    print(f"📦 新版本: {new_version}")
    print()
    
    # 显示总结
    print("=" * 70)
    print("✨ 升级总结")
    print("=" * 70)
    print(f"📦 包名称: {package_name}")
    print(f"📊 升级前: {current_version}")
    print(f"📊 升级后: {new_version}")
    print("=" * 70)
    print()
    
    # 测试 claude 命令是否可用
    print("🔍 测试 claude 命令...")
    returncode, stdout, stderr = run_command(["claude", "--version"], env, timeout=10)
    
    if returncode == 0:
        print(f"✅ claude 命令可用: {stdout.strip()}")
    else:
        print("⚠️  claude 命令测试失败")
        print(f"错误信息: {stderr}")
    
    print()
    return True

def check_all_versions(script_dir: Path, available_venvs: List[Tuple[str, str, str]], package_name: str) -> dict:
    """
    检查所有虚拟环境的版本信息
    返回: {venv_name: {"current": version, "latest": version, "has_update": bool}}
    """
    version_info = {}
    latest_version = None
    
    print("🔍 正在检查所有虚拟环境的版本...")
    print()
    
    for venv_name, bin_subdir, display_name in available_venvs:
        venv_path = script_dir / venv_name
        venv_bin_dir = venv_path / bin_subdir
        is_windows = (venv_name == "venv_win")
        
        # 设置环境变量
        env = os.environ.copy()
        env["VIRTUAL_ENV"] = str(venv_path)
        env["NPM_CONFIG_PREFIX"] = str(venv_path)
        
        # 更新 PATH
        venv_bin = str(venv_bin_dir)
        if "PATH" in env:
            path_separator = ";" if is_windows else ":"
            env["PATH"] = f"{venv_bin}{path_separator}{env['PATH']}"
        else:
            env["PATH"] = venv_bin
        
        # 获取当前版本
        current_version = get_npm_package_version(package_name, env)
        
        # 只需要查询一次最新版本（使用 npm view 获取最新版本）
        if latest_version is None:
            # 先尝试使用 npm view 获取最新版本
            returncode, stdout, stderr = run_command(
                ["npm", "view", package_name, "version"],
                env,
                timeout=60
            )
            
            if returncode == 0 and stdout:
                latest_version = stdout.strip()
            else:
                # 如果 npm view 失败，尝试使用 npm outdated
                returncode, stdout, stderr = run_command(
                    ["npm", "outdated", "-g", package_name, "--json"],
                    env,
                    timeout=60
                )
                
                if stdout:
                    try:
                        data = json.loads(stdout)
                        if package_name in data:
                            latest_version = data[package_name].get("latest", "unknown")
                    except:
                        pass
            
            if latest_version is None:
                latest_version = "unknown"
        
        has_update = False
        if current_version != "未安装" and latest_version != "unknown":
            has_update = (current_version != latest_version)
        
        version_info[venv_name] = {
            "current": current_version,
            "latest": latest_version,
            "has_update": has_update,
            "display_name": display_name
        }
    
    return version_info

def main():
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    
    # 获取当前系统信息
    current_venv_name, current_bin_subdir, is_windows = get_platform_info()
    current_system = "Windows" if is_windows else "macOS"
    
    print("=" * 70)
    print("🔄 Claude Code 虚拟环境升级工具")
    print("=" * 70)
    print(f"📍 脚本目录: {script_dir}")
    print(f"💻 当前系统: {platform.system()} ({current_system})")
    print("=" * 70)
    print()
    
    # 获取可用的虚拟环境
    available_venvs = get_available_venvs(script_dir)
    
    if not available_venvs:
        print("❌ 错误：没有找到任何虚拟环境")
        print("\n💡 请先创建虚拟环境")
        sys.exit(1)
    
    # 检查所有虚拟环境的版本
    package_name = "@anthropic-ai/claude-code"
    version_info = check_all_versions(script_dir, available_venvs, package_name)
    
    # 显示版本信息表格
    print("=" * 70)
    print("📊 版本信息")
    print("=" * 70)
    for venv_name, bin_subdir, display_name in available_venvs:
        info = version_info[venv_name]
        status = " ✨ (当前系统)" if venv_name == current_venv_name else ""
        
        print(f"\n📦 {display_name} ({venv_name}){status}")
        print(f"   当前版本: {info['current']}")
        print(f"   最新版本: {info['latest']}")
        
        if info['current'] == "未安装":
            print(f"   状态: ⚠️  未安装")
        elif info['has_update']:
            print(f"   状态: 🔄 有更新可用")
        else:
            print(f"   状态: ✅ 已是最新")
    
    print()
    print("=" * 70)
    print()
    
    # 重新排序：当前系统的虚拟环境放在第一位
    sorted_venvs = []
    other_venvs = []
    
    for venv_info in available_venvs:
        if venv_info[0] == current_venv_name:
            sorted_venvs.insert(0, venv_info)
        else:
            other_venvs.append(venv_info)
    
    sorted_venvs.extend(other_venvs)
    
    # 显示选项
    print("请选择要升级的虚拟环境：")
    for i, (venv_name, _, display_name) in enumerate(sorted_venvs, 1):
        recommended = " (推荐)" if venv_name == current_venv_name else ""
        print(f"   {i}. {display_name}{recommended}")
    
    if len(sorted_venvs) > 1:
        print(f"   {len(sorted_venvs) + 1}. 全部升级")
    
    print(f"   q. 退出")
    
    print()
    
    # 获取用户选择
    while True:
        try:
            choice = input("请输入选项编号 (直接回车选择推荐选项): ").strip().lower()
            
            # 如果直接回车，选择第一个（推荐）选项
            if not choice:
                choice = "1"
            
            # 检查是否退出
            if choice in ['q', 'quit', 'exit']:
                print("\n👋 退出升级工具")
                sys.exit(0)
            
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(sorted_venvs):
                selected_venvs = [sorted_venvs[choice_num - 1]]
                break
            elif choice_num == len(sorted_venvs) + 1 and len(sorted_venvs) > 1:
                selected_venvs = sorted_venvs
                break
            else:
                max_option = len(sorted_venvs) + 1 if len(sorted_venvs) > 1 else len(sorted_venvs)
                print(f"❌ 无效选项，请输入 1-{max_option} 或 q 退出")
        except ValueError:
            print("❌ 请输入有效的数字或 q 退出")
        except KeyboardInterrupt:
            print("\n\n❌ 用户取消操作")
            sys.exit(0)
    
    print()
    
    # 确认升级
    if len(selected_venvs) == 1:
        venv_name, _, display_name = selected_venvs[0]
        print(f"📦 将升级 {display_name} 虚拟环境")
    else:
        print(f"📦 将升级 {len(selected_venvs)} 个虚拟环境")
    
    user_input = input("是否继续？(y/n): ").strip().lower()
    
    if user_input not in ['y', 'yes', '是']:
        print("\n❌ 用户取消操作")
        sys.exit(0)
    
    # 执行升级
    success_count = 0
    fail_count = 0
    
    for venv_name, bin_subdir, display_name in selected_venvs:
        try:
            if upgrade_venv(script_dir, venv_name, bin_subdir, display_name, package_name):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"\n❌ 升级 {display_name} 时发生错误: {e}")
            fail_count += 1
    
    # 显示最终总结
    print()
    print("=" * 70)
    print("🎉 升级流程完成！")
    print("=" * 70)
    print(f"✅ 成功: {success_count} 个")
    if fail_count > 0:
        print(f"❌ 失败: {fail_count} 个")
    print("=" * 70)
    print()
    print("💡 提示：")
    print("   - 使用 'python run.py' 启动 Claude Code")
    print("   - 使用 'python update.py' 再次升级")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
