#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🎨 项目启动器 - 主题样式库
灵感来自: Oh My Zsh, Starship, Powerlevel10k 等流行主题
"""

from inquirer.themes import Theme


class DefaultTheme(Theme):
    """默认主题 - 柔和的蓝紫色"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[96m'  # 青色
        self.Question.brackets_color = '\033[94m'  # 蓝色
        self.Question.default_color = '\033[37m'  # 白色
        self.List.selection_color = '\033[95m'  # 紫色
        self.List.selection_cursor = '❯'
        self.List.unselected_color = '\033[37m'  # 白色
        
        # 自定义属性 - 用于项目列表显示
        self.accent_color = '\033[95m'  # 强调色
        self.text_color = '\033[37m'  # 文本色
        self.dim_color = '\033[90m'  # 暗淡色


class OceanTheme(Theme):
    """海洋主题 - 蓝绿色系"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[96m'  # 青色
        self.Question.brackets_color = '\033[36m'  # 深青色
        self.Question.default_color = '\033[97m'  # 亮白
        self.List.selection_color = '\033[1;96m'  # 亮青色 + 加粗
        self.List.selection_cursor = '🌊'
        self.List.unselected_color = '\033[36m'  # 深青色
        
        self.accent_color = '\033[96m'
        self.text_color = '\033[36m'
        self.dim_color = '\033[34m'


class SunsetTheme(Theme):
    """日落主题 - 橙红色系"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[93m'  # 黄色
        self.Question.brackets_color = '\033[91m'  # 红色
        self.Question.default_color = '\033[97m'  # 亮白
        self.List.selection_color = '\033[1;93m'  # 亮黄 + 加粗
        self.List.selection_cursor = '🔥'
        self.List.unselected_color = '\033[33m'  # 深黄
        
        self.accent_color = '\033[93m'
        self.text_color = '\033[33m'
        self.dim_color = '\033[90m'


class ForestTheme(Theme):
    """森林主题 - 绿色系"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[92m'  # 绿色
        self.Question.brackets_color = '\033[32m'  # 深绿
        self.Question.default_color = '\033[97m'  # 亮白
        self.List.selection_color = '\033[1;92m'  # 亮绿 + 加粗
        self.List.selection_cursor = '🌲'
        self.List.unselected_color = '\033[32m'  # 深绿
        
        self.accent_color = '\033[92m'
        self.text_color = '\033[32m'
        self.dim_color = '\033[90m'


class NeonTheme(Theme):
    """霓虹主题 - 高对比度"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[1;95m'  # 亮紫 + 加粗
        self.Question.brackets_color = '\033[1;93m'  # 亮黄 + 加粗
        self.Question.default_color = '\033[1;97m'  # 亮白 + 加粗
        self.List.selection_color = '\033[1;96m'  # 亮青 + 加粗
        self.List.selection_cursor = '⚡'
        self.List.unselected_color = '\033[90m'  # 灰色
        
        self.accent_color = '\033[1;95m'
        self.text_color = '\033[96m'
        self.dim_color = '\033[90m'


class MinimalTheme(Theme):
    """极简主题 - 黑白灰"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[37m'  # 白色
        self.Question.brackets_color = '\033[90m'  # 灰色
        self.Question.default_color = '\033[37m'  # 白色
        self.List.selection_color = '\033[1;37m'  # 亮白 + 加粗
        self.List.selection_cursor = '►'
        self.List.unselected_color = '\033[90m'  # 灰色
        
        self.accent_color = '\033[37m'
        self.text_color = '\033[37m'
        self.dim_color = '\033[90m'


class GalaxyTheme(Theme):
    """星系主题 - 深紫蓝"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[1;94m'  # 亮蓝 + 加粗
        self.Question.brackets_color = '\033[95m'  # 紫色
        self.Question.default_color = '\033[97m'  # 亮白
        self.List.selection_color = '\033[1;95m'  # 亮紫 + 加粗
        self.List.selection_cursor = '⭐'
        self.List.unselected_color = '\033[94m'  # 蓝色
        
        self.accent_color = '\033[95m'
        self.text_color = '\033[94m'
        self.dim_color = '\033[90m'


class CyberpunkTheme(Theme):
    """赛博朋克主题 - 粉紫青"""
    def __init__(self):
        super().__init__()
        self.Question.mark_color = '\033[1;96m'  # 亮青 + 加粗
        self.Question.brackets_color = '\033[95m'  # 紫色
        self.Question.default_color = '\033[1;97m'  # 亮白 + 加粗
        self.List.selection_color = '\033[1;95m'  # 亮紫 + 加粗
        self.List.selection_cursor = '▶'
        self.List.unselected_color = '\033[96m'  # 青色
        
        self.accent_color = '\033[1;95m'
        self.text_color = '\033[96m'
        self.dim_color = '\033[90m'


# 主题映射
THEMES = {
    'default': DefaultTheme,
    'ocean': OceanTheme,
    'sunset': SunsetTheme,
    'forest': ForestTheme,
    'neon': NeonTheme,
    'minimal': MinimalTheme,
    'galaxy': GalaxyTheme,
    'cyberpunk': CyberpunkTheme,
}

# 主题描述
THEME_DESCRIPTIONS = {
    'default': '默认 - 柔和蓝紫色 ❯',
    'ocean': '海洋 - 清新蓝绿色 🌊',
    'sunset': '日落 - 温暖橙红色 🔥',
    'forest': '森林 - 自然绿色系 🌲',
    'neon': '霓虹 - 高对比炫彩 ⚡',
    'minimal': '极简 - 黑白灰调 ►',
    'galaxy': '星系 - 深邃紫蓝 ⭐',
    'cyberpunk': '赛博朋克 - 未来感 ▶',
}


def get_theme(theme_name='default'):
    """获取主题实例"""
    theme_class = THEMES.get(theme_name.lower(), DefaultTheme)
    return theme_class()


def list_themes():
    """列出所有主题"""
    print("\n🎨 可用主题:\n")
    for name, desc in THEME_DESCRIPTIONS.items():
        print(f"  • {name:12s} - {desc}")
    print()

