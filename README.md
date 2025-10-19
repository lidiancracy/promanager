# promanager

🚀 **项目启动器** - 一个强大的命令行项目管理工具

## ✨ 功能特性

- 🎯 **智能管理** - 统一管理所有开发项目
- 🚀 **快速打开** - 一键用不同 IDE 打开项目（IDEA/VSCode/WebStorm/Cursor）
- 📦 **批量操作** - 批量打开/删除多个项目
- 🔍 **智能搜索** - 模糊匹配、实时补全
- ⭐ **置顶功能** - 重要项目置顶显示
- 📊 **统计分析** - 打开次数统计，智能排序
- 🎨 **精美主题** - 8种主题可选
- 💻 **跨平台** - 支持 Windows

## 📦 安装

### 方式 1：使用打包好的 exe（推荐）

1. 下载 `deploy` 目录下的所有文件
2. 编辑 `config.json` 配置 IDE 路径
3. 运行 `一键安装.bat`
4. 重新打开 CMD，输入 `open` 开始使用

### 方式 2：从源码运行

```bash
# 克隆仓库
git clone git@github.com:lidiancracy/promanager.git
cd promanager

# 安装依赖
pip install inquirer prompt_toolkit

# 运行
python open.py
```

## 🎮 快速开始

```bash
# 启动交互式主菜单
open

# 批量选择打开项目
open ls

# 批量删除项目
open rm

# 添加当前目录为项目
open add

# 切换主题
open style

# 查看帮助
open help
```

## 💡 使用示例

### 批量打开项目

```bash
$ open ls

# 步骤1: 看到所有项目列表
# 步骤2: 输入 shop → 选择 → 已选 1 个
# 步骤3: 输入 admin → 选择 → 已选 2 个
# 步骤4: 直接回车 → 确认 → 批量打开所有项目
```

### 批量删除项目

```bash
$ open rm

# 步骤1: 显示所有项目列表
# 步骤2: 输入项目名搜索并选择
# 步骤3: 添加到删除列表
# 步骤4: 直接回车或输入 yes 确认删除
```

## 🎨 主题预览

- **default** - 默认蓝紫色
- **ocean** - 海洋蓝绿色 🌊
- **sunset** - 日落橙红色 🔥
- **forest** - 森林绿色系 🌲
- **neon** - 霓虹炫彩 ⚡
- **minimal** - 极简黑白 ►
- **galaxy** - 星系紫蓝 ⭐
- **cyberpunk** - 赛博朋克 ▶

## 📖 命令列表

| 命令 | 说明 |
|------|------|
| `open` | 启动交互式主菜单 |
| `open ls` | 批量选择打开项目 |
| `open rm` | 批量删除项目 |
| `open add` | 添加当前目录为项目 |
| `open style` | 切换主题风格 |
| `open stats` | 查看统计信息 |
| `open config` | 打开配置文件 |
| `open help` | 查看完整帮助 |

## 🛠️ 技术栈

- Python 3.9+
- inquirer - 交互式命令行界面
- prompt_toolkit - 自动补全和输入提示
- PyInstaller - 打包成 exe

## 📁 项目结构

```
promanager/
├── open.py              # 主程序
├── themes.py            # 主题文件
├── config.example.json  # 配置示例
├── open.spec           # PyInstaller 打包配置
├── install.bat         # 安装脚本
├── deploy/             # 部署文件夹
│   ├── open.exe        # 打包好的程序
│   ├── config.json     # IDE 配置
│   ├── themes.py       # 主题文件
│   ├── 一键安装.bat     # 一键安装
│   ├── 测试运行.bat     # 测试脚本
│   └── 使用说明.txt     # 使用说明
└── README.md           # 说明文档
```

## ⚙️ 配置文件

配置文件位置：
- **IDE 配置**: `程序所在目录/config.json`
- **项目数据**: `~/.project-manager/projects.json`

`config.json` 示例：
```json
{
  "ide_paths": {
    "idea": "D:\\Program Files\\JetBrains\\IntelliJ IDEA\\bin\\idea64.exe",
    "vscode": "C:\\Program Files\\Microsoft VS Code\\Code.exe",
    "webstorm": "D:\\Program Files\\JetBrains\\WebStorm\\bin\\webstorm64.exe",
    "cursor": "cursor"
  },
  "default_ide": "idea"
}
```

## 🔧 从源码打包

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包
pyinstaller open.spec

# 打包后的文件在 dist 目录
```

## ❓ 常见问题

**Q: 提示找不到 open 命令？**  
A: 重新打开 CMD 窗口，让 PATH 生效

**Q: 无法打开项目？**  
A: 检查 config.json 中的 IDE 路径是否正确

**Q: 如何卸载？**  
A: 删除文件夹，从环境变量 PATH 中移除路径即可

## 📝 更新日志

### v1.1.0 (2025-10-19)
- ✅ 新增批量删除功能 (`open rm`)
- ✅ 优化确认逻辑（支持回车和 yes）
- ✅ 更新帮助文档

### v1.0.0 (2025-10-19)
- ✅ 初始版本发布
- ✅ 支持多 IDE 管理
- ✅ 批量打开项目
- ✅ 8种主题可选
- ✅ 智能搜索和补全

## 📄 许可证

MIT License

## 👨‍💻 作者

lidiancracy

## 🙏 致谢

感谢以下开源项目：
- [inquirer](https://github.com/magmax/python-inquirer)
- [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)
- [PyInstaller](https://github.com/pyinstaller/pyinstaller)

---

⭐ 如果觉得有用，请给个 Star！
