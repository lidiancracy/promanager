#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试导入是否成功"""

print("开始测试导入...")

try:
    import inquirer
    print("✅ inquirer 导入成功")
    print(f"   版本: {inquirer.__version__ if hasattr(inquirer, '__version__') else '未知'}")
    print(f"   路径: {inquirer.__file__}")
except ImportError as e:
    print(f"❌ inquirer 导入失败: {e}")
except Exception as e:
    print(f"❌ inquirer 异常: {e}")

try:
    from inquirer.themes import Theme
    print("✅ inquirer.themes 导入成功")
except ImportError as e:
    print(f"❌ inquirer.themes 导入失败: {e}")

try:
    from prompt_toolkit import prompt
    print("✅ prompt_toolkit 导入成功")
    print(f"   路径: {prompt.__module__}")
except ImportError as e:
    print(f"❌ prompt_toolkit 导入失败: {e}")

try:
    import readchar
    print("✅ readchar 导入成功")
except ImportError as e:
    print(f"❌ readchar 导入失败: {e}")

try:
    import blessed
    print("✅ blessed 导入成功")
except ImportError as e:
    print(f"❌ blessed 导入失败: {e}")

print("\n所有测试完成!")

