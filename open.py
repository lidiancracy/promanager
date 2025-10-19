#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🚀 项目启动器 - 交互式命令行版
简单、直观、高效
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import inquirer
    from inquirer.themes import Theme
    HAS_INQUIRER = True
except ImportError:
    HAS_INQUIRER = False
    print("❌ 缺少 inquirer 库,请安装:")
    print("   pip install inquirer prompt_toolkit")
    print()
    sys.exit(1)
except Exception as e:
    HAS_INQUIRER = False
    print(f"❌ inquirer 导入失败: {e}")
    print("💡 请尝试:")
    print("   pip install --upgrade inquirer prompt_toolkit")
    print()
    sys.exit(1)

# 导入主题
try:
    from themes import get_theme, list_themes, THEME_DESCRIPTIONS
    HAS_THEMES = True
except ImportError:
    HAS_THEMES = False
    # 降级到内置主题
    class CustomTheme(Theme):
        def __init__(self):
            super().__init__()
            self.Question.mark_color = '\033[96m'
            self.Question.brackets_color = '\033[94m'
            self.Question.default_color = '\033[37m'
            self.List.selection_color = '\033[95m'
            self.List.selection_cursor = '❯'
            self.List.unselected_color = '\033[37m'
    
    def get_theme(name='default'):
        return CustomTheme()
    
    class CustomTheme:
        """内置默认主题(当 themes.py 不存在时)"""
        def __init__(self):
            self.accent_color = '\033[95m'
            self.text_color = '\033[37m'
            self.dim_color = '\033[90m'

try:
    from prompt_toolkit import prompt
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.document import Document
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False

# 配置文件路径
CONFIG_DIR = Path.home() / '.project-manager'
CONFIG_FILE = CONFIG_DIR / 'projects.json'
IDE_CONFIG_FILE = CONFIG_DIR / 'ide_config.json'

# 尝试从当前目录加载 IDE 配置
SCRIPT_DIR = Path(__file__).parent
LOCAL_IDE_CONFIG = SCRIPT_DIR / 'config.json'

# 默认配置
DEFAULT_CONFIG = {
    "settings": {
        "default_ide": "idea",
        "theme": "default",
        "ide_paths": {
            "idea": r"D:\code\IntelliJ IDEA 2024.3.5\bin\idea64.exe",
            "vscode": r"C:\Program Files\Microsoft VS Code\Code.exe",
            "webstorm": r"D:\code\webstorm\WebStorm 2025.1.4.1\bin\webstorm64.exe",
            "cursor": "cursor"
        }
    },
    "projects": []
}

def load_ide_config():
    """加载 IDE 配置,优先级:本地 config.json > 用户目录 > 默认"""
    # 1. 优先读取脚本目录的 config.json
    if LOCAL_IDE_CONFIG.exists():
        try:
            with open(LOCAL_IDE_CONFIG, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('ide_paths', {}), config.get('default_ide', 'idea')
        except Exception as e:
            print(f"⚠️  读取本地配置失败: {e}")
    
    # 2. 读取用户目录的配置
    if IDE_CONFIG_FILE.exists():
        try:
            with open(IDE_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('ide_paths', {}), config.get('default_ide', 'idea')
        except Exception as e:
            print(f"⚠️  读取用户配置失败: {e}")
    
    # 3. 使用默认配置
    return DEFAULT_CONFIG['settings']['ide_paths'], DEFAULT_CONFIG['settings']['default_ide']

# IDE 图标和颜色
IDE_ICONS = {
    "idea": "💡",
    "vscode": "📘",
    "webstorm": "🌊",
    "cursor": "⚡"
}

# ANSI 颜色代码
IDE_COLORS = {
    "idea": "\033[94m",      # 蓝色
    "vscode": "\033[96m",    # 青色
    "webstorm": "\033[91m",  # 红色
    "cursor": "\033[95m",    # 紫色
}
COLOR_RESET = "\033[0m"


def print_banner(title, width=70):
    """打印漂亮的 Banner"""
    padding = (width - len(title) - 4) // 2
    print("\n╔" + "═" * width + "╗")
    print("║" + " " * padding + title + " " * (width - padding - len(title)) + "║")
    print("╚" + "═" * width + "╝")


def print_separator(width=70):
    """打印分隔线"""
    print("─" * width)


class ProjectCompleter(Completer):
    """项目自动补全器 - 实时过滤"""
    def __init__(self, projects):
        self.projects = projects
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lower()
        
        for project in self.projects:
            # 匹配名称、别名、描述
            name = project['name']
            alias = project.get('alias', '')
            remark = project.get('remark', '')
            
            if (text in name.lower() or 
                text in alias.lower() or 
                text in remark.lower()):
                
                display = f"{name}"
                if alias and alias != name:
                    display += f" ({alias})"
                if remark:
                    display += f" - {remark[:30]}"
                
                yield Completion(
                    text=alias or name,
                    start_position=-len(text),
                    display=display
                )


class ProjectManager:
    def __init__(self):
        self.config = self.load_config()
        # 加载 IDE 配置并更新
        ide_paths, default_ide = load_ide_config()
        if 'settings' not in self.config:
            self.config['settings'] = {}
        self.config['settings']['ide_paths'] = ide_paths
        self.config['settings']['default_ide'] = default_ide
        
        # 加载主题
        theme_name = self.config.get('settings', {}).get('theme', 'default')
        self.theme = get_theme(theme_name)
    
    def load_config(self):
        """加载配置"""
        if not CONFIG_FILE.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
            return DEFAULT_CONFIG.copy()
        
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_config(self):
        """保存配置"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_sorted_projects(self):
        """获取排序后的项目(置顶 + 打开次数)"""
        projects = self.config['projects']
        pinned = [p for p in projects if p.get('pinned', False)]
        unpinned = [p for p in projects if not p.get('pinned', False)]
        
        pinned.sort(key=lambda x: x.get('open_count', 0), reverse=True)
        unpinned.sort(key=lambda x: x.get('open_count', 0), reverse=True)
        
        return pinned + unpinned
    
    def format_project_display(self, project, with_color=True):
        """格式化项目显示"""
        pin = "⭐" if project.get('pinned', False) else "  "
        ide_key = project.get('ide', 'idea')
        ide = IDE_ICONS.get(ide_key, '📁')
        name = project.get('alias', project['name'])[:30]
        count = project.get('open_count', 0)
        remark = project.get('remark', '')[:40]
        
        # 应用颜色
        if with_color:
            color = IDE_COLORS.get(ide_key, "")
            display = f"{pin} {ide} {color}{name:<30}{COLOR_RESET} "
        else:
            display = f"{pin} {ide} {name:<30} "
        
        if remark:
            display += f"[{remark}] "
        display += f"(打开{count}次)"
        
        return display
    
    def open_project(self, project):
        """打开项目"""
        ide = project.get('ide', self.config['settings']['default_ide'])
        ide_path = self.config['settings']['ide_paths'].get(ide)
        
        if not ide_path:
            print(f"\n❌ 未配置 {ide.upper()} 路径")
            input("\n按回车继续...")
            return False
        
        project_path = project['path']
        
        print(f"\n{IDE_ICONS.get(ide, '📁')} 正在用 {ide.upper()} 打开...")
        print(f"📂 {project['name']}")
        print(f"📁 {project_path}")
        
        try:
            if ide == 'cursor':
                subprocess.Popen([ide_path, project_path], 
                               shell=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([ide_path, project_path],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            
            # 更新打开次数
            project['open_count'] = project.get('open_count', 0) + 1
            project['last_opened'] = datetime.now().isoformat()
            self.save_config()
            
            print("✅ 已打开!")
            return True
        except Exception as e:
            print(f"❌ 打开失败: {e}")
            return False
    
    def open_project_silent(self, project):
        """静默打开项目(用于批量打开)"""
        ide = project.get('ide', self.config['settings']['default_ide'])
        ide_path = self.config['settings']['ide_paths'].get(ide)
        
        if not ide_path:
            return False
        
        try:
            if ide == 'cursor':
                subprocess.Popen([ide_path, project['path']], 
                               shell=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen([ide_path, project['path']],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            
            # 更新打开次数
            project['open_count'] = project.get('open_count', 0) + 1
            project['last_opened'] = datetime.now().isoformat()
            return True
        except:
            return False
    
    def show_main_menu(self):
        """主菜单 - 交互式选择项目"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            projects = self.get_sorted_projects()
            
            if not projects:
                print_banner("🚀 项目启动器", 70)
                print("\n📭 还没有项目\n")
                
                questions = [
                    inquirer.List('action',
                                message="要做什么?",
                                choices=[
                                    ('➕ 添加项目', 'add'),
                                    ('⚙️  配置 IDE 路径', 'config'),
                                    ('❌ 退出', 'exit')
                                ])
                ]
                
                answer = inquirer.prompt(questions, theme=self.theme)
                if not answer or answer['action'] == 'exit':
                    print("\n👋 再见!")
                    break
                elif answer['action'] == 'add':
                    self.add_project()
                elif answer['action'] == 'config':
                    self.open_config()
                continue
            
            # 显示项目列表
            print_banner("🚀 项目启动器", 70)
            
            # 构建选项
            choices = []
            
            # 分组显示
            pinned = [p for p in projects if p.get('pinned', False)]
            unpinned = [p for p in projects if not p.get('pinned', False)]
            
            if pinned:
                choices.append(inquirer.Separator('\n⭐ 置顶项目'))
                for p in pinned:
                    choices.append((self.format_project_display(p), p))
            
            if unpinned:
                choices.append(inquirer.Separator('\n📌 全部项目'))
                for p in unpinned:
                    choices.append((self.format_project_display(p), p))
            
            # 底部操作
            choices.append(inquirer.Separator('\n' + '─' * 70))
            choices.extend([
                ('➕ 添加新项目', 'add'),
                ('📊 查看统计', 'stats'),
                ('⚙️  配置设置', 'config'),
                ('❌ 退出', 'exit')
            ])
            
            questions = [
                inquirer.List('project',
                            message="选择项目 (↑↓ 选择, Enter 打开, Ctrl+C 退出)",
                            choices=choices,
                            carousel=True)
            ]
            
            try:
                answer = inquirer.prompt(questions, theme=self.theme)
                
                if not answer:
                    print("\n👋 再见!")
                    break
                
                selected = answer['project']
                
                if selected == 'exit':
                    print("\n👋 再见!")
                    break
                elif selected == 'add':
                    self.add_project()
                elif selected == 'stats':
                    self.show_stats()
                elif selected == 'config':
                    self.open_config()
                elif isinstance(selected, dict):
                    # 选中了项目,显示项目操作菜单
                    self.show_project_menu(selected)
            
            except KeyboardInterrupt:
                print("\n\n👋 再见!")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")
                input("\n按回车继续...")
    
    def show_project_menu(self, project):
        """项目操作菜单"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print_banner(f"📁 {project['name']}", 70)
            print(f"\n别名: {project.get('alias', '-')}")
            print(f"路径: {project['path']}")
            print(f"IDE:  {IDE_ICONS.get(project.get('ide', 'idea'), '📁')} {project.get('ide', 'idea').upper()}")
            print(f"描述: {project.get('remark', '-')}")
            print(f"打开: {project.get('open_count', 0)} 次")
            print(f"置顶: {'是 ⭐' if project.get('pinned', False) else '否'}")
            
            # 构建操作选项
            choices = [
                (f"🚀 用 {project.get('ide', 'idea').upper()} 打开", 'open_default'),
            ]
            
            # 添加其他 IDE 选项
            current_ide = project.get('ide', 'idea')
            for ide in ['idea', 'webstorm', 'cursor']:
                if ide != current_ide:
                    choices.append((f"{IDE_ICONS[ide]} 用 {ide.upper()} 打开", f'open_{ide}'))
            
            choices.extend([
                inquirer.Separator(''),
                ('⭐ 置顶' if not project.get('pinned', False) else '📌 取消置顶', 'toggle_pin'),
                ('✏️  编辑信息', 'edit'),
                ('🗑️  删除项目', 'delete'),
                inquirer.Separator(''),
                ('⬅️  返回', 'back')
            ])
            
            questions = [
                inquirer.List('action',
                            message="选择操作",
                            choices=choices,
                            carousel=True)
            ]
            
            try:
                answer = inquirer.prompt(questions, theme=self.theme)
                
                if not answer or answer['action'] == 'back':
                    break
                
                action = answer['action']
                
                if action == 'open_default':
                    self.open_project(project)
                    input("\n按回车继续...")
                    break
                elif action.startswith('open_'):
                    ide = action.replace('open_', '')
                    original_ide = project['ide']
                    project['ide'] = ide
                    self.open_project(project)
                    project['ide'] = original_ide
                    input("\n按回车继续...")
                    break
                elif action == 'toggle_pin':
                    project['pinned'] = not project.get('pinned', False)
                    self.save_config()
                    status = "置顶" if project['pinned'] else "取消置顶"
                    print(f"\n✅ 已{status}")
                    input("\n按回车继续...")
                elif action == 'edit':
                    self.edit_project(project)
                elif action == 'delete':
                    if self.confirm_delete(project):
                        self.config['projects'].remove(project)
                        self.save_config()
                        print("\n✅ 已删除")
                        input("\n按回车继续...")
                        break
            
            except KeyboardInterrupt:
                break
    
    def add_project(self, path=None):
        """添加项目 - 简化版"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print_banner("➕ 添加新项目", 70)
        
        # 获取路径
        if path is None:
            path = os.getcwd()
        
        path = os.path.abspath(path)
        
        if not os.path.exists(path):
            print(f"❌ 路径不存在: {path}")
            input("\n按回车继续...")
            return
        
        # 检查是否已存在
        for p in self.config['projects']:
            if p['path'] == path:
                print(f"⚠️  该路径已存在: {p['name']}")
                input("\n按回车继续...")
                return
        
        print(f"📂 项目路径: {path}\n")
        
        try:
            # 简化的问题列表
            questions = [
                inquirer.Text('name',
                            message="项目名称",
                            default=os.path.basename(path)),
                inquirer.Text('alias',
                            message="别名 (可选,方便快速搜索)",
                            default=""),
                inquirer.Text('remark',
                            message="描述 (可选)",
                            default=""),
                inquirer.List('ide',
                            message="默认 IDE",
                            choices=[
                                ('💡 IntelliJ IDEA', 'idea'),
                                ('📘 VSCode', 'vscode'),
                                ('🌊 WebStorm', 'webstorm'),
                                ('⚡ Cursor', 'cursor')
                            ],
                            default='idea')
            ]
            
            answers = inquirer.prompt(questions, theme=self.theme)
            
            if not answers:
                print("\n❌ 已取消")
                input("\n按回车继续...")
                return
            
            # 检查别名是否重复
            alias = answers['alias'] or answers['name']
            for p in self.config['projects']:
                if p.get('alias', '') == alias and alias:
                    print(f"\n⚠️  别名 '{alias}' 已存在,请使用其他别名")
                    input("\n按回车继续...")
                    return
            
            # 创建项目
            project = {
                "name": answers['name'],
                "alias": alias,
                "path": path,
                "ide": answers['ide'],
                "remark": answers['remark'],
                "pinned": False,
                "open_count": 0,
                "created_at": datetime.now().isoformat()
            }
            
            self.config['projects'].append(project)
            self.save_config()
            
            print(f"\n✅ 项目已添加: {answers['name']}")
            input("\n按回车继续...")
        
        except KeyboardInterrupt:
            print("\n\n❌ 已取消")
            input("\n按回车继续...")
    
    def edit_project(self, project):
        """编辑项目"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print_banner(f"✏️  编辑项目: {project['name']}", 70)
        
        try:
            questions = [
                inquirer.Text('name',
                            message="项目名称",
                            default=project['name']),
                inquirer.Text('alias',
                            message="别名",
                            default=project.get('alias', '')),
                inquirer.Text('remark',
                            message="描述",
                            default=project.get('remark', '')),
                inquirer.List('ide',
                            message="默认 IDE",
                            choices=[
                                ('💡 IntelliJ IDEA', 'idea'),
                                ('📘 VSCode', 'vscode'),
                                ('🌊 WebStorm', 'webstorm'),
                                ('⚡ Cursor', 'cursor')
                            ],
                            default=project.get('ide', 'idea'))
            ]
            
            answers = inquirer.prompt(questions, theme=self.theme)
            
            if answers:
                project['name'] = answers['name']
                project['alias'] = answers['alias']
                project['remark'] = answers['remark']
                project['ide'] = answers['ide']
                self.save_config()
                
                print("\n✅ 已保存")
                input("\n按回车继续...")
        
        except KeyboardInterrupt:
            print("\n\n❌ 已取消")
            input("\n按回车继续...")
    
    def confirm_delete(self, project):
        """确认删除"""
        questions = [
            inquirer.Confirm('confirm',
                           message=f"确定要删除项目 '{project['name']}' 吗?",
                           default=False)
        ]
        
        answer = inquirer.prompt(questions, theme=self.theme)
        return answer and answer['confirm']
    
    def show_stats(self):
        """显示统计信息"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        projects = self.config['projects']
        
        print_banner("📊 统计信息", 70)
        
        if not projects:
            print("📭 还没有项目\n")
        else:
            total = len(projects)
            pinned = len([p for p in projects if p.get('pinned', False)])
            total_opens = sum(p.get('open_count', 0) for p in projects)
            
            # IDE 统计
            ide_stats = {}
            for p in projects:
                ide = p.get('ide', 'idea')
                ide_stats[ide] = ide_stats.get(ide, 0) + 1
            
            # 最常用项目
            top_projects = sorted(projects, key=lambda x: x.get('open_count', 0), reverse=True)[:5]
            
            print(f"📁 总项目数:   {total}")
            print(f"⭐ 置顶项目:   {pinned}")
            print(f"🚀 总打开次数: {total_opens}\n")
            
            print("💡 IDE 分布:")
            for ide, count in ide_stats.items():
                emoji = IDE_ICONS.get(ide, '📁')
                print(f"  {emoji} {ide.upper():10s}: {count} 个")
            
            if top_projects and total_opens > 0:
                print("\n🔥 最常用项目:")
                for i, p in enumerate(top_projects, 1):
                    if p.get('open_count', 0) > 0:
                        emoji = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
                        print(f"  {i}. {emoji} {p['name']:20s} - {p.get('open_count', 0)} 次")
        
        print("\n" + "─" * 70)
        input("\n按回车返回...")
    
    def open_config(self):
        """打开配置文件"""
        print(f"\n📁 配置文件: {CONFIG_FILE}")
        try:
            if os.name == 'nt':
                os.startfile(CONFIG_FILE)
            else:
                subprocess.call(['open', CONFIG_FILE])
            print("✅ 已打开配置文件")
        except Exception as e:
            print(f"❌ 无法打开: {e}")
        
        input("\n按回车继续...")
    
    def change_theme(self):
        """更改主题"""
        if not HAS_THEMES:
            print("\n⚠️  主题文件不存在,使用默认主题")
            input("\n按回车继续...")
            return
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner("🎨 选择主题", 70)
        
        # 列出所有主题
        print("\n📋 可用主题:\n")
        choices = []
        for name, desc in THEME_DESCRIPTIONS.items():
            choices.append((f"{desc}", name))
        
        current_theme = self.config.get('settings', {}).get('theme', 'default')
        
        questions = [
            inquirer.List('theme',
                        message=f"当前主题: {current_theme}",
                        choices=choices,
                        carousel=True)
        ]
        
        try:
            answer = inquirer.prompt(questions, theme=self.theme)
            
            if answer:
                new_theme = answer['theme']
                
                # 更新配置
                if 'settings' not in self.config:
                    self.config['settings'] = {}
                self.config['settings']['theme'] = new_theme
                self.save_config()
                
                # 更新当前主题
                self.theme = get_theme(new_theme)
                
                print(f"\n✅ 主题已切换为: {new_theme}")
                print("💡 新主题将在下次运行时生效")
                input("\n按回车继续...")
        
        except KeyboardInterrupt:
            print("\n\n❌ 已取消")
            input("\n按回车继续...")


    def quick_remove_batch(self):
        """批量选择删除项目 - 类似 open ls 的交互方式"""
        selected_projects = []
        all_projects = self.get_sorted_projects()
        
        if not all_projects:
            print("\n📭 还没有项目")
            input("\n按回车继续...")
            return
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner("🗑️  批量删除项目", 70)
            
            # 显示所有项目列表(应用主题颜色)
            accent = getattr(self.theme, 'accent_color', '\033[95m')
            text = getattr(self.theme, 'text_color', '\033[37m')
            dim = getattr(self.theme, 'dim_color', '\033[90m')
            reset = '\033[0m'
            
            print(f"\n{accent}📋 所有项目:{reset}\n")
            for p in all_projects[:15]:
                alias = f"{dim}({p.get('alias', '')}){reset}" if p.get('alias') else ""
                remark = f"{dim}- {p.get('remark', '')}{reset}" if p.get('remark') else ""
                ide = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
                pin = "⭐" if p.get('pinned', False) else "  "
                name_color = accent if p.get('pinned', False) else text
                print(f"{pin} {ide} {name_color}{p['name']}{reset} {alias} {remark}")
            
            if len(all_projects) > 15:
                print(f"{dim}  ... 还有 {len(all_projects) - 15} 个项目{reset}")
            
            print("\n" + "─" * 70)
            
            # 显示已选择要删除的项目(应用主题色)
            if selected_projects:
                print(f"\n{accent}❌ 待删除 {len(selected_projects)} 个项目:{reset}")
                for i, p in enumerate(selected_projects, 1):
                    ide_emoji = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
                    alias_display = f" {dim}({p.get('alias', '')}){reset}" if p.get('alias') and p.get('alias') != p['name'] else ""
                    print(f"  {accent}{i}.{reset} {ide_emoji} {text}{p['name']}{reset}{alias_display}")
                print("\n" + "─" * 70)
            
            # 输入搜索
            print(f"\n💡 输入项目名搜索 | 直接回车{accent}删除{reset}已选项目 | Ctrl+C 退出\n")
            
            try:
                search_input = prompt("🔍 搜索: ", 
                                     completer=ProjectCompleter([p for p in all_projects if p not in selected_projects])).strip()
                
                if not search_input:
                    # 直接回车,删除已选项目
                    break
                
                # 搜索匹配(排除已选)
                # 精确匹配别名或名称
                exact_match = None
                for p in all_projects:
                    if p not in selected_projects:
                        if (p.get('alias', '').lower() == search_input.lower() or 
                            p['name'].lower() == search_input.lower()):
                            exact_match = p
                            break
                
                if exact_match:
                    # 精确匹配,直接添加
                    selected_projects.append(exact_match)
                    continue
                
                # 模糊匹配
                search_lower = search_input.lower()
                matched = [p for p in all_projects 
                          if (search_lower in p['name'].lower() or 
                              search_lower in p.get('alias', '').lower() or
                              search_lower in p.get('remark', '').lower())
                          and p not in selected_projects]
                
                if not matched:
                    print(f"\n❌ 找不到匹配 '{search_input}' 的未选项目")
                    input("\n按回车继续...")
                    continue
                elif len(matched) == 1:
                    # 只有1个匹配,直接添加
                    selected_projects.append(matched[0])
                    continue
                else:
                    # 多个匹配,显示选择列表
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner(f"🔍 搜索: {search_input} (共 {len(matched)} 个)", 70)
                    
                    if selected_projects:
                        print(f"\n❌ 待删除: {', '.join([p['name'] for p in selected_projects])}\n")
                    
                    choices = [(self.format_project_display(p), p) for p in matched]
                    
                    questions = [
                        inquirer.List('project',
                                    message="↑↓ 选择项目,回车添加到删除列表",
                                    choices=choices,
                                    carousel=True)
                    ]
                    
                    answer = inquirer.prompt(questions, theme=self.theme)
                    
                    if answer and answer['project']:
                        selected_projects.append(answer['project'])
            
            except KeyboardInterrupt:
                print("\n\n❌ 已取消")
                return
            except EOFError:
                break
        
        # 删除选中的项目
        if not selected_projects:
            print("\n⚠️  未选择任何项目")
            input("\n按回车继续...")
            return
        
        # 确认并删除
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner(f"⚠️  确认删除 {len(selected_projects)} 个项目", 70)
        
        print("\n❌ 将要删除的项目:\n")
        for i, p in enumerate(selected_projects, 1):
            ide_emoji = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
            alias_display = f"({p.get('alias', '')})" if p.get('alias') and p.get('alias') != p['name'] else ""
            remark = f"- {p.get('remark', '')}" if p.get('remark') else ""
            print(f"  {i}. {ide_emoji} {p['name']}{alias_display} {remark}")
        
        print("\n" + "─" * 70)
        print("⚠️  警告: 删除操作无法撤销!")
        print("─" * 70)
        confirm = input("\n按回车或输入 yes 确认删除 (输入 n 取消): ").strip().lower()
        
        if confirm != 'n':
            print(f"\n🗑️  正在删除 {len(selected_projects)} 个项目...\n")
            
            success_count = 0
            for i, project in enumerate(selected_projects, 1):
                ide_emoji = IDE_ICONS.get(project.get('ide', 'idea'), '📁')
                print(f"[{i}/{len(selected_projects)}] {ide_emoji} {project['name']}...", end=" ", flush=True)
                
                try:
                    self.config['projects'].remove(project)
                    print("✅")
                    success_count += 1
                except:
                    print("❌")
            
            # 保存配置
            self.save_config()
            
            print(f"\n✅ 成功删除 {success_count}/{len(selected_projects)} 个项目!")
        else:
            print("\n❌ 已取消删除")
        
        input("\n按回车继续...")

    def quick_open_batch(self):
        """批量选择打开项目 - 简化流程"""
        selected_projects = []
        all_projects = self.get_sorted_projects()
        
        if not all_projects:
            print("\n📭 还没有项目")
            input("\n按回车继续...")
            return
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner("🚀 批量选择项目", 70)
            
            # 显示所有项目列表(应用主题颜色)
            accent = getattr(self.theme, 'accent_color', '\033[95m')
            text = getattr(self.theme, 'text_color', '\033[37m')
            dim = getattr(self.theme, 'dim_color', '\033[90m')
            reset = '\033[0m'
            
            print(f"\n{accent}📋 所有项目:{reset}\n")
            for p in all_projects[:15]:
                alias = f"{dim}({p.get('alias', '')}){reset}" if p.get('alias') else ""
                remark = f"{dim}- {p.get('remark', '')}{reset}" if p.get('remark') else ""
                ide = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
                pin = "⭐" if p.get('pinned', False) else "  "
                name_color = accent if p.get('pinned', False) else text
                print(f"{pin} {ide} {name_color}{p['name']}{reset} {alias} {remark}")
            
            if len(all_projects) > 15:
                print(f"{dim}  ... 还有 {len(all_projects) - 15} 个项目{reset}")
            
            print("\n" + "─" * 70)
            
            # 显示已选择的项目(应用主题色)
            if selected_projects:
                print(f"\n{accent}✅ 已选择 {len(selected_projects)} 个项目:{reset}")
                for i, p in enumerate(selected_projects, 1):
                    ide_emoji = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
                    alias_display = f" {dim}({p.get('alias', '')}){reset}" if p.get('alias') and p.get('alias') != p['name'] else ""
                    print(f"  {accent}{i}.{reset} {ide_emoji} {text}{p['name']}{reset}{alias_display}")
                print("\n" + "─" * 70)
            
            # 输入搜索
            print("\n💡 输入项目名搜索 | 直接回车打开已选项目 | Ctrl+C 退出\n")
            
            try:
                search_input = prompt("🔍 搜索: ", 
                                     completer=ProjectCompleter([p for p in all_projects if p not in selected_projects])).strip()
                
                if not search_input:
                    # 直接回车,打开已选项目
                    break
                
                # 搜索匹配(排除已选)
                # 精确匹配别名或名称
                exact_match = None
                for p in all_projects:
                    if p not in selected_projects:
                        if (p.get('alias', '').lower() == search_input.lower() or 
                            p['name'].lower() == search_input.lower()):
                            exact_match = p
                            break
                
                if exact_match:
                    # 精确匹配,直接添加
                    selected_projects.append(exact_match)
                    continue
                
                # 模糊匹配
                search_lower = search_input.lower()
                matched = [p for p in all_projects 
                          if (search_lower in p['name'].lower() or 
                              search_lower in p.get('alias', '').lower() or
                              search_lower in p.get('remark', '').lower())
                          and p not in selected_projects]
                
                if not matched:
                    print(f"\n❌ 找不到匹配 '{search_input}' 的未选项目")
                    input("\n按回车继续...")
                    continue
                elif len(matched) == 1:
                    # 只有1个匹配,直接添加
                    selected_projects.append(matched[0])
                    continue
                else:
                    # 多个匹配,显示选择列表
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner(f"🔍 搜索: {search_input} (共 {len(matched)} 个)", 70)
                    
                    if selected_projects:
                        print(f"\n✅ 已选择: {', '.join([p['name'] for p in selected_projects])}\n")
                    
                    choices = [(self.format_project_display(p), p) for p in matched]
                    
                    questions = [
                        inquirer.List('project',
                                    message="↑↓ 选择项目,回车添加",
                                    choices=choices,
                                    carousel=True)
                    ]
                    
                    answer = inquirer.prompt(questions, theme=self.theme)
                    
                    if answer and answer['project']:
                        selected_projects.append(answer['project'])
            
            except KeyboardInterrupt:
                print("\n\n❌ 已取消")
                return
            except EOFError:
                break
        
        # 打开选中的项目
        if not selected_projects:
            print("\n⚠️  未选择任何项目")
            input("\n按回车继续...")
            return
        
        # 确认并打开
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner(f"📋 确认打开 {len(selected_projects)} 个项目", 70)
        
        print("\n✅ 将要打开的项目:\n")
        for i, p in enumerate(selected_projects, 1):
            ide_emoji = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
            alias_display = f"({p.get('alias', '')})" if p.get('alias') and p.get('alias') != p['name'] else ""
            remark = f"- {p.get('remark', '')}" if p.get('remark') else ""
            print(f"  {i}. {ide_emoji} {p['name']}{alias_display} {remark}")
        
        print("\n" + "─" * 70)
        confirm = input("\n按回车开始打开所有项目 (输入 n 取消): ").strip().lower()
        
        if confirm != 'n':
            print(f"\n🚀 正在打开 {len(selected_projects)} 个项目...\n")
            
            success_count = 0
            for i, project in enumerate(selected_projects, 1):
                ide_emoji = IDE_ICONS.get(project.get('ide', 'idea'), '📁')
                print(f"[{i}/{len(selected_projects)}] {ide_emoji} {project['name']}...", end=" ", flush=True)
                
                if self.open_project_silent(project):
                    print("✅")
                    success_count += 1
                else:
                    print("❌")
            
            # 保存配置(统一保存一次)
            self.save_config()
            
            print(f"\n✅ 成功打开 {success_count}/{len(selected_projects)} 个项目!")
        else:
            print("\n❌ 已取消")
        
        input("\n按回车继续...")
    
    def quick_open(self, keyword=None, multi_select=False):
        """快速打开 - 带实时搜索过滤"""
        projects = self.get_sorted_projects()
        
        if not projects:
            print("\n📭 还没有项目")
            input("\n按回车继续...")
            return
        
        # 如果没有提供关键词且支持实时搜索
        if not keyword and HAS_PROMPT_TOOLKIT:
            self._interactive_search(projects, multi_select)
        else:
            # 传统模式:先过滤再选择
            if keyword:
                keyword_lower = keyword.lower()
                filtered = [p for p in projects 
                           if keyword_lower in p['name'].lower() 
                           or keyword_lower in p.get('alias', '').lower()
                           or keyword_lower in p.get('remark', '').lower()]
                
                if not filtered:
                    print(f"\n❌ 找不到匹配 '{keyword}' 的项目")
                    input("\n按回车继续...")
                    return
                
                projects = filtered
            
            self._select_and_open(projects, keyword, multi_select)
    
    def _interactive_search(self, all_projects, multi_select=False):
        """交互式实时搜索"""
        from prompt_toolkit.shortcuts import input_dialog
        from prompt_toolkit.styles import Style
        from prompt_toolkit.formatted_text import HTML
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print_banner("🚀 快速打开 - 实时搜索", 70)
            
            # 显示所有项目
            pinned = [p for p in all_projects if p.get('pinned', False)]
            unpinned = [p for p in all_projects if not p.get('pinned', False)]
            
            if pinned:
                print("\n⭐ 置顶项目:")
                for i, p in enumerate(pinned[:5], 1):
                    print(f"  {self.format_project_display(p)}")
            
            if unpinned:
                print("\n📌 全部项目:" if pinned else "\n📌 项目列表:")
                for i, p in enumerate(unpinned[:10], 1):
                    print(f"  {self.format_project_display(p)}")
                
                if len(unpinned) > 10:
                    print(f"  ... 还有 {len(unpinned) - 10} 个项目")
            
            print("\n" + "─" * 70)
            print("💡 输入关键词过滤 | 留空查看全部 | Ctrl+C 退出")
            print("─" * 70)
            
            try:
                keyword = prompt("\n🔍 搜索: ", completer=ProjectCompleter(all_projects)).strip()
                
                # 过滤项目
                if keyword:
                    keyword_lower = keyword.lower()
                    filtered = [p for p in all_projects 
                               if keyword_lower in p['name'].lower() 
                               or keyword_lower in p.get('alias', '').lower()
                               or keyword_lower in p.get('remark', '').lower()]
                    
                    if not filtered:
                        print(f"\n❌ 找不到匹配 '{keyword}' 的项目")
                        input("\n按回车继续...")
                        continue
                    
                    projects = filtered
                else:
                    projects = all_projects
                
                # 选择并打开
                self._select_and_open(projects, keyword, multi_select)
                break
                
            except KeyboardInterrupt:
                print("\n\n❌ 已取消")
                break
            except EOFError:
                projects = all_projects
                self._select_and_open(projects, None, multi_select)
                break
    
    def _select_and_open(self, projects, keyword=None, multi_select=False):
        """选择并打开项目 - 支持连续选择累加"""
        selected_projects = []
        all_projects = self.get_sorted_projects()  # 获取所有项目用于搜索
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_banner("🚀 选择项目", 70)
            
            # 显示已选择的项目
            if selected_projects:
                print(f"\n✅ 已选择 {len(selected_projects)} 个项目:")
                for i, p in enumerate(selected_projects, 1):
                    ide_emoji = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
                    print(f"  {i}. {ide_emoji} {p['name']}")
                print("\n" + "─" * 70)
            
            # 提示
            print("\n💡 输入项目名称搜索 | 留空完成选择并打开 | Ctrl+C 退出\n")
            
            try:
                # 输入搜索关键词,带自动补全
                search_input = prompt("🔍 搜索项目: ", 
                                     completer=ProjectCompleter(all_projects)).strip()
                
                if not search_input:
                    # 留空表示完成选择
                    break
                
                # 搜索匹配的项目
                search_lower = search_input.lower()
                matched = [p for p in all_projects 
                          if (search_lower in p['name'].lower() or 
                              search_lower in p.get('alias', '').lower() or
                              search_lower in p.get('remark', '').lower())
                          and p not in selected_projects]  # 排除已选
                
                if not matched:
                    print(f"\n❌ 找不到匹配 '{search_input}' 的项目")
                    input("\n按回车继续...")
                    continue
                
                # 显示匹配结果并选择
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner(f"🔍 搜索: {search_input} (共 {len(matched)} 个)", 70)
                
                if selected_projects:
                    print(f"\n✅ 已选择: ", end="")
                    print(", ".join([p['name'] for p in selected_projects]))
                    print()
                
                choices = [(self.format_project_display(p), p) for p in matched]
                
                questions = [
                    inquirer.List('project',
                                message="选择一个项目添加到列表",
                                choices=choices,
                                carousel=True)
                ]
                
                answer = inquirer.prompt(questions, theme=self.theme)
                
                if answer and answer['project']:
                    # 添加到已选列表
                    selected_projects.append(answer['project'])
                    # 不需要 input,直接循环回到开始,会显示已选项目
            
            except KeyboardInterrupt:
                print("\n\n❌ 已取消")
                return
            except EOFError:
                break
        
        # 完成选择,开始打开
        if not selected_projects:
            print("\n⚠️  未选择任何项目")
            input("\n按回车继续...")
            return
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner(f"📋 确认打开 {len(selected_projects)} 个项目", 70)
        
        print("\n✅ 将要打开的项目:\n")
        for i, p in enumerate(selected_projects, 1):
            ide_emoji = IDE_ICONS.get(p.get('ide', 'idea'), '📁')
            print(f"  {i}. {ide_emoji} {p['name']} - {p.get('remark', '')}")
        
        print("\n" + "─" * 70)
        confirm = input("\n按回车开始打开所有项目 (输入 n 取消): ").strip().lower()
        
        if confirm != 'n':
            print(f"\n🚀 正在打开 {len(selected_projects)} 个项目...\n")
            for i, project in enumerate(selected_projects, 1):
                print(f"[{i}/{len(selected_projects)}] 打开 {project['name']}...")
                self.open_project(project)
            
            print(f"\n✅ 已打开 {len(selected_projects)} 个项目!")
        else:
            print("\n❌ 已取消")
        
        input("\n按回车继续...")


def main():
    if not HAS_INQUIRER:
        return
    
    manager = ProjectManager()
    
    args = sys.argv[1:]
    
    # 快捷命令
    if args:
        cmd = args[0].lower()
        
        if cmd == 'list' or cmd == 'ls':
            # open list/ls - 批量选择打开
            manager.quick_open_batch()
            return
        elif cmd == 'remove' or cmd == 'rm' or cmd == 'del':
            # open rm/remove/del - 批量删除项目
            manager.quick_remove_batch()
            return
        elif cmd == 'add':
            path = args[1] if len(args) > 1 else None
            manager.add_project(path)
            return
        elif cmd == 'config':
            manager.open_config()
            return
        elif cmd == 'stats':
            manager.show_stats()
            return
        elif cmd == 'style' or cmd == 'theme':
            manager.change_theme()
            return
        elif cmd == 'help':
            print("""
╔══════════════════════════════════════════════════════════╗
║              🚀 项目启动器 - 使用指南                     ║
╚══════════════════════════════════════════════════════════╝

📖 基本用法:

  open                启动交互式主菜单
  open list           批量选择打开项目
  open ls             同 list (简写)
  open rm             批量删除项目
  open add            添加当前目录为项目
  open style          更换主题风格
  open stats          查看统计信息
  open config         打开配置文件

💡 交互式操作:

  主菜单模式 (open):
  • 使用 ↑↓ 方向键选择项目
  • 按 Enter 进入项目操作菜单
  • 可以进行详细操作:
    - 打开项目(多种 IDE)
    - 置顶/取消置顶
    - 编辑信息
    - 删除项目

  批量选择模式 (open list / open ls):
  
  流程:
  1. 显示所有项目(名称+别名+描述)
  2. 输入项目名搜索 → ↑↓选择 → 回车添加
  3. 显示已选: 1. xxx  2. yyy  3. zzz
  4. 继续输入搜索下一个项目,或直接回车
  5. 回车后确认并批量打开所有项目
  
  批量删除模式 (open rm):
  
  流程:
  1. 显示所有项目列表
  2. 输入项目名搜索 → ↑↓选择 → 回车添加到删除列表
  3. 显示待删除: 1. xxx  2. yyy  3. zzz
  4. 继续输入搜索下一个,或直接回车
  5. 回车或输入 yes 确认删除(输入 n 取消)

🎯 特性:

  • 实时补全: 输入时动态提示项目名
  • 连续选择: 逐个搜索累加项目
  • 智能排序: 按打开次数自动排序
  • 批量打开: 一次打开多个项目
  • 模糊搜索: 支持名称/别名/描述
  • 多 IDE:   支持 IDEA/VSCode/WebStorm/Cursor
  • 颜色区分: 不同 IDE 不同颜色
  • 多种主题: 8种精美主题可选

🎨 主题风格:

  open style          查看并切换主题
  
  可用主题:
  • default   - 默认蓝紫色
  • ocean     - 海洋蓝绿色 🌊
  • sunset    - 日落橙红色 🔥
  • forest    - 森林绿色系 🌲
  • neon      - 霓虹炫彩 ⚡
  • minimal   - 极简黑白 ►
  • galaxy    - 星系紫蓝 ⭐
  • cyberpunk - 赛博朋克 ▶

📝 使用示例:

  open ls (批量打开)
  步骤1: 看到所有项目列表
  步骤2: 输入 shop → 选择 → 已选 1 个
  步骤3: 输入 admin → 选择 → 已选 2 个
  步骤4: 输入 api → 选择 → 已选 3 个
  步骤5: 直接回车 → 确认 → 批量打开 3 个项目
  
  open rm (批量删除)
  步骤1: 看到所有项目列表
  步骤2: 输入 test → 选择 → 待删除 1 个
  步骤3: 输入 demo → 选择 → 待删除 2 个
  步骤4: 直接回车 → 直接回车或输入 yes → 删除完成

配置文件: {config_file}

════════════════════════════════════════════════════════════
""".format(config_file=CONFIG_FILE))
            return
    
    # 启动主菜单
    manager.show_main_menu()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见!")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
