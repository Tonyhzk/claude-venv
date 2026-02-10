#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 Claude Code 缓存文件脚本
用于在分发项目前清理个人使用痕迹和缓存数据
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


class ClaudeCacheCleaner:
    """Claude 缓存清理器"""
    
    def __init__(self, claude_dir: str = "claude-code-venv/.claude"):
        """
        初始化清理器
        
        Args:
            claude_dir: .claude 目录路径
        """
        self.base_dir = Path(__file__).parent.parent
        self.claude_dir = self.base_dir / claude_dir
        self.cleaned_items = []
        self.errors = []
        self.preview_items = []  # 预览列表
        
    def get_size(self, path: Path) -> int:
        """获取文件或目录大小"""
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            total = 0
            for item in path.rglob('*'):
                if item.is_file():
                    try:
                        total += item.stat().st_size
                    except:
                        pass
            return total
        return 0
    
    def format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
    
    def clean_backup_files(self, preview_only=False):
        """清理 .claude.json 备份文件"""
        if not preview_only:
            print("🧹 清理备份文件...")
        pattern = ".claude.json.backup.*"
        
        for backup_file in self.claude_dir.glob(pattern):
            if preview_only:
                size = self.get_size(backup_file)
                self.preview_items.append({
                    'path': backup_file.relative_to(self.base_dir),
                    'size': size,
                    'type': '备份文件'
                })
            else:
                try:
                    backup_file.unlink()
                    self.cleaned_items.append(str(backup_file.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: {backup_file.name}")
                except Exception as e:
                    self.errors.append(f"删除 {backup_file.name} 失败: {e}")
                    print(f"  ✗ 失败: {backup_file.name}")
    
    def clean_history(self, preview_only=False):
        """清理历史记录"""
        if not preview_only:
            print("\n🧹 清理历史记录...")
        history_file = self.claude_dir / "history.jsonl"
        
        if history_file.exists():
            if preview_only:
                size = self.get_size(history_file)
                self.preview_items.append({
                    'path': history_file.relative_to(self.base_dir),
                    'size': size,
                    'type': '历史记录'
                })
            else:
                try:
                    history_file.unlink()
                    self.cleaned_items.append(str(history_file.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: history.jsonl")
                except Exception as e:
                    self.errors.append(f"删除 history.jsonl 失败: {e}")
                    print(f"  ✗ 失败: history.jsonl")
    
    def clean_stats_cache(self, preview_only=False):
        """清理统计缓存"""
        if not preview_only:
            print("\n🧹 清理统计缓存...")
        stats_file = self.claude_dir / "stats-cache.json"
        
        if stats_file.exists():
            if preview_only:
                size = self.get_size(stats_file)
                self.preview_items.append({
                    'path': stats_file.relative_to(self.base_dir),
                    'size': size,
                    'type': '统计缓存'
                })
            else:
                try:
                    stats_file.unlink()
                    self.cleaned_items.append(str(stats_file.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: stats-cache.json")
                except Exception as e:
                    self.errors.append(f"删除 stats-cache.json 失败: {e}")
                    print(f"  ✗ 失败: stats-cache.json")
    
    def clean_cache_dir(self, preview_only=False):
        """清理 cache 目录"""
        if not preview_only:
            print("\n🧹 清理缓存目录...")
        cache_dir = self.claude_dir / "cache"
        
        if cache_dir.exists():
            if preview_only:
                size = self.get_size(cache_dir)
                self.preview_items.append({
                    'path': cache_dir.relative_to(self.base_dir),
                    'size': size,
                    'type': '缓存目录'
                })
            else:
                try:
                    shutil.rmtree(cache_dir)
                    self.cleaned_items.append(str(cache_dir.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: cache/ 目录")
                except Exception as e:
                    self.errors.append(f"删除 cache/ 目录失败: {e}")
                    print(f"  ✗ 失败: cache/ 目录")
    
    def clean_debug_dir(self, preview_only=False):
        """清理 debug 目录"""
        if not preview_only:
            print("\n🧹 清理调试日志...")
        debug_dir = self.claude_dir / "debug"
        
        if debug_dir.exists():
            if preview_only:
                size = self.get_size(debug_dir)
                self.preview_items.append({
                    'path': debug_dir.relative_to(self.base_dir),
                    'size': size,
                    'type': '调试日志'
                })
            else:
                try:
                    shutil.rmtree(debug_dir)
                    self.cleaned_items.append(str(debug_dir.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: debug/ 目录")
                except Exception as e:
                    self.errors.append(f"删除 debug/ 目录失败: {e}")
                    print(f"  ✗ 失败: debug/ 目录")
    
    def clean_projects_dir(self, preview_only=False):
        """清理 projects 目录（会话数据）"""
        if not preview_only:
            print("\n🧹 清理项目会话数据...")
        projects_dir = self.claude_dir / "projects"
        
        if projects_dir.exists():
            if preview_only:
                size = self.get_size(projects_dir)
                self.preview_items.append({
                    'path': projects_dir.relative_to(self.base_dir),
                    'size': size,
                    'type': '会话数据'
                })
            else:
                try:
                    shutil.rmtree(projects_dir)
                    self.cleaned_items.append(str(projects_dir.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: projects/ 目录")
                except Exception as e:
                    self.errors.append(f"删除 projects/ 目录失败: {e}")
                    print(f"  ✗ 失败: projects/ 目录")
    
    def clean_telemetry_dir(self, preview_only=False):
        """清理 telemetry 目录"""
        if not preview_only:
            print("\n🧹 清理遥测数据...")
        telemetry_dir = self.claude_dir / "telemetry"
        
        if telemetry_dir.exists():
            if preview_only:
                size = self.get_size(telemetry_dir)
                self.preview_items.append({
                    'path': telemetry_dir.relative_to(self.base_dir),
                    'size': size,
                    'type': '遥测数据'
                })
            else:
                try:
                    shutil.rmtree(telemetry_dir)
                    self.cleaned_items.append(str(telemetry_dir.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: telemetry/ 目录")
                except Exception as e:
                    self.errors.append(f"删除 telemetry/ 目录失败: {e}")
                    print(f"  ✗ 失败: telemetry/ 目录")
    
    def clean_todos_dir(self, preview_only=False):
        """清理 todos 目录"""
        if not preview_only:
            print("\n🧹 清理待办事项...")
        todos_dir = self.claude_dir / "todos"
        
        if todos_dir.exists():
            if preview_only:
                size = self.get_size(todos_dir)
                self.preview_items.append({
                    'path': todos_dir.relative_to(self.base_dir),
                    'size': size,
                    'type': '待办事项'
                })
            else:
                try:
                    shutil.rmtree(todos_dir)
                    self.cleaned_items.append(str(todos_dir.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: todos/ 目录")
                except Exception as e:
                    self.errors.append(f"删除 todos/ 目录失败: {e}")
                    print(f"  ✗ 失败: todos/ 目录")
    
    def clean_plugin_cache(self, preview_only=False):
        """清理插件缓存"""
        if not preview_only:
            print("\n🧹 清理插件缓存...")
        plugin_cache_dir = self.claude_dir / "plugins" / "cache"
        
        if plugin_cache_dir.exists():
            if preview_only:
                size = self.get_size(plugin_cache_dir)
                self.preview_items.append({
                    'path': plugin_cache_dir.relative_to(self.base_dir),
                    'size': size,
                    'type': '插件缓存'
                })
            else:
                try:
                    shutil.rmtree(plugin_cache_dir)
                    self.cleaned_items.append(str(plugin_cache_dir.relative_to(self.base_dir)))
                    print(f"  ✓ 删除: plugins/cache/ 目录")
                except Exception as e:
                    self.errors.append(f"删除 plugins/cache/ 目录失败: {e}")
                    print(f"  ✗ 失败: plugins/cache/ 目录")
    
    def clean_git_repos(self, preview_only=False):
        """清理插件市场的 .git 目录"""
        if not preview_only:
            print("\n🧹 清理 Git 仓库数据...")
        marketplaces_dir = self.claude_dir / "plugins" / "marketplaces"
        
        if marketplaces_dir.exists():
            git_dirs = list(marketplaces_dir.rglob(".git"))
            for git_dir in git_dirs:
                if preview_only:
                    size = self.get_size(git_dir)
                    self.preview_items.append({
                        'path': git_dir.relative_to(self.base_dir),
                        'size': size,
                        'type': 'Git仓库'
                    })
                else:
                    try:
                        shutil.rmtree(git_dir)
                        self.cleaned_items.append(str(git_dir.relative_to(self.base_dir)))
                        print(f"  ✓ 删除: {git_dir.relative_to(self.claude_dir)}")
                    except Exception as e:
                        self.errors.append(f"删除 {git_dir.relative_to(self.claude_dir)} 失败: {e}")
                        print(f"  ✗ 失败: {git_dir.relative_to(self.claude_dir)}")
    
    def generate_report(self):
        """生成清理报告"""
        print("\n" + "="*60)
        print("📊 清理报告")
        print("="*60)
        print(f"✓ 成功清理: {len(self.cleaned_items)} 项")
        print(f"✗ 失败: {len(self.errors)} 项")
        
        if self.cleaned_items:
            print("\n已清理的项目:")
            for item in self.cleaned_items:
                print(f"  • {item}")
        
        if self.errors:
            print("\n清理失败的项目:")
            for error in self.errors:
                print(f"  • {error}")
        
        # 保存报告到文件
        report_file = self.base_dir / "2_Scripts" / f"cache_clean_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Claude Code 缓存清理报告\n")
            f.write(f"清理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(f"成功清理: {len(self.cleaned_items)} 项\n")
            f.write(f"失败: {len(self.errors)} 项\n\n")
            
            if self.cleaned_items:
                f.write("已清理的项目:\n")
                for item in self.cleaned_items:
                    f.write(f"  • {item}\n")
            
            if self.errors:
                f.write("\n清理失败的项目:\n")
                for error in self.errors:
                    f.write(f"  • {error}\n")
        
        print(f"\n📄 详细报告已保存到: {report_file.name}")
    
    def preview_cleanup(self):
        """预览将要清理的文件"""
        print("="*60)
        print("🔍 扫描缓存文件...")
        print("="*60)
        
        # 预览模式扫描所有文件
        self.clean_backup_files(preview_only=True)
        self.clean_history(preview_only=True)
        self.clean_stats_cache(preview_only=True)
        self.clean_cache_dir(preview_only=True)
        self.clean_debug_dir(preview_only=True)
        self.clean_projects_dir(preview_only=True)
        self.clean_telemetry_dir(preview_only=True)
        self.clean_todos_dir(preview_only=True)
        self.clean_plugin_cache(preview_only=True)
        self.clean_git_repos(preview_only=True)
        
        if not self.preview_items:
            print("\n✨ 没有发现需要清理的缓存文件！")
            return False
        
        # 显示预览列表
        print(f"\n📋 发现 {len(self.preview_items)} 项可清理内容：")
        print("="*60)
        
        total_size = 0
        for item in self.preview_items:
            total_size += item['size']
            print(f"[{item['type']}] {item['path']}")
            print(f"  大小: {self.format_size(item['size'])}")
            print()
        
        print("="*60)
        print(f"📊 总计: {len(self.preview_items)} 项，共 {self.format_size(total_size)}")
        print("="*60)
        
        return True
    
    def run(self):
        """执行清理"""
        print("="*60)
        print("🚀 Claude Code 缓存清理工具")
        print("="*60)
        print(f"目标目录: {self.claude_dir}")
        print()
        
        if not self.claude_dir.exists():
            print(f"❌ 错误: 目录不存在 - {self.claude_dir}")
            return
        
        # 先预览
        has_items = self.preview_cleanup()
        
        if not has_items:
            return
        
        # 询问确认
        print("\n⚠️  警告: 以上文件将被永久删除！")
        print("💡 提示: 以下文件将被保留：")
        print("  • .claude.json 和 settings.json 配置文件")
        print("  • 插件配置文件")
        print("  • 插件市场内容（仅删除 .git 目录）")
        print()
        
        try:
            confirm = input("❓ 确认删除？(输入 y 继续，其他任意键取消): ").strip().lower()
        except KeyboardInterrupt:
            print("\n\n❌ 已取消清理操作")
            return
        
        if confirm != 'y':
            print("\n❌ 已取消清理操作")
            return
        
        print("\n" + "="*60)
        print("🧹 开始清理...")
        print("="*60)
        
        # 执行各项清理任务
        self.clean_backup_files()
        self.clean_history()
        self.clean_stats_cache()
        self.clean_cache_dir()
        self.clean_debug_dir()
        self.clean_projects_dir()
        self.clean_telemetry_dir()
        self.clean_todos_dir()
        self.clean_plugin_cache()
        self.clean_git_repos()
        
        # 生成报告
        self.generate_report()
        
        print("\n✅ 清理完成！")


def main():
    """主函数"""
    cleaner = ClaudeCacheCleaner()
    cleaner.run()


if __name__ == "__main__":
    main()
