# 🚀 项目启动器 - 一键部署版

> 一个优雅的命令行项目管理工具,让你在 CMD 中快速打开和管理项目

---

## ⚡ 30秒快速部署

### 步骤 0: 确认环境(仅exe版可跳过)

如果你的电脑**没有 Python**:
- ✅ 直接跳到步骤 1
- ✅ exe 版无需任何依赖

如果你的电脑**有 Python** 且想用 Python 版:
- 查看 `deploy-python` 文件夹
- 更轻量,启动稍慢,可自定义

### 步骤 1: 配置 IDE 路径

用记事本打开 **`config.json`**,修改为你的实际路径:

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

**重要**: Windows 路径必须用 `\\` 双斜杠!

### 步骤 2: 安装

双击运行 **`一键安装.bat`**

### 步骤 3: 开始使用

**重新打开 CMD 窗口**,然后输入:

```cmd
open help
```

搞定! 🎉

---

## 📖 核心功能

### 🎯 批量选择打开项目

```cmd
open ls
```

**流程**:
1. 显示所有项目列表
2. 输入项目名搜索(实时补全提示)
3. 上下键选择,回车添加
4. 继续搜索添加更多项目
5. 留空回车 → 批量打开所有选中的项目

### ➕ 添加项目

```cmd
cd C:\Projects\my-project
open add
```

输入:
- 项目名称
- 别名(方便搜索)
- 描述
- 选择 IDE

### 🎨 切换主题

```cmd
open style
```

8 种精美主题可选:
- 🎨 default - 柔和蓝紫(默认)
- 🌊 ocean - 清新蓝绿
- 🔥 sunset - 温暖橙红
- 🌲 forest - 自然绿色
- ⚡ neon - 霓虹炫彩
- ► minimal - 极简黑白
- ⭐ galaxy - 深邃紫蓝
- ▶ cyberpunk - 赛博朋克

---

## 🎮 所有命令

```cmd
open          # 主菜单(交互式管理)
open ls       # 批量选择打开
open add      # 添加项目
open style    # 切换主题
open stats    # 查看统计
open config   # 打开配置文件
open help     # 查看帮助
```

---

## ✨ 核心特性

- ✅ **智能排序** - 常用项目自动靠前
- ✅ **置顶功能** - 重要项目始终在顶部
- ✅ **批量打开** - 一次打开多个项目
- ✅ **实时搜索** - 输入时动态提示
- ✅ **模糊匹配** - 支持名称/别名/描述
- ✅ **多IDE支持** - IDEA/VSCode/WebStorm/Cursor
- ✅ **主题切换** - 8种风格随心选
- ✅ **别名系统** - 快速搜索定位
- ✅ **配置独立** - 易于跨电脑部署

---

## 📋 部署清单

在新电脑部署时需要:

1. ✅ 复制整个文件夹
2. ✅ 编辑 `config.json` (修改IDE路径)
3. ✅ 运行 `一键安装.bat`
4. ✅ 重开 CMD

---

## 🧪 测试运行(无需安装)

如果想先测试功能,双击 **`测试运行.bat`**

会打开一个临时 CMD 环境,可以直接测试所有命令,关闭后不影响系统。

---

## 📁 文件说明

| 文件 | 必需 | 说明 |
|------|------|------|
| open.exe | ✅ | 主程序,约7MB |
| config.json | ✅ | IDE路径配置 |
| themes.py | ✅ | 主题文件,8种风格 |
| 一键安装.bat | 推荐 | 自动安装脚本 |
| 使用说明.txt | - | 快速参考 |

**注意**: `open.exe` 和 `themes.py` 必须在同一目录!

---

## ⚙️ 如何找IDE路径?

### IntelliJ IDEA
1. 右键桌面快捷方式 → 属性 → 查看"目标"
2. 或者默认路径:
   ```
   D:\Program Files\JetBrains\IntelliJ IDEA 2024.x\bin\idea64.exe
   ```

### VSCode
默认路径:
```
C:\Program Files\Microsoft VS Code\Code.exe
```

或用户安装:
```
C:\Users\你的用户名\AppData\Local\Programs\Microsoft VS Code\Code.exe
```

### WebStorm
类似 IDEA:
```
D:\Program Files\JetBrains\WebStorm 2024.x\bin\webstorm64.exe
```

---

## 💾 数据存储位置

**项目数据**:
```
C:\Users\你的用户名\.project-manager\projects.json
```

所有添加的项目信息都存在这里,可以:
- 直接编辑
- 备份
- 复制到其他电脑

**IDE配置**:
```
程序所在目录\config.json
```

---

## 🔄 多电脑同步

### 方案 1: 手动同步
复制 `C:\Users\你的用户名\.project-manager\projects.json` 到其他电脑相同位置

### 方案 2: 统一部署
在每台电脑上:
1. 放到相同位置(如 `C:\Tools\project-manager\`)
2. 修改 `config.json` 为对应电脑的 IDE 路径
3. 运行安装脚本

---

## 🎯 使用技巧

### 技巧 1: 快速打开单个项目
```cmd
open ls
输入: shop
回车(精确匹配直接添加) → 留空回车 → 打开
```

### 技巧 2: 批量打开工作区
```cmd
open ls
输入: front → 选前端项目
输入: back → 选后端项目
输入: doc → 选文档项目
留空回车 → 一次性打开3个项目
```

### 技巧 3: 置顶常用项目
进入主菜单 `open` → 选择项目 → 选择"置顶"
置顶的项目会始终显示在列表最上方

---

## 🛠️ 故障排除

### 问题: 命令找不到
**解决**:
1. 确认已运行安装脚本
2. 重新打开 CMD 窗口
3. 检查环境变量 PATH 是否包含程序目录

### 问题: IDE 无法打开
**解决**:
1. 确认 IDE 已安装
2. 检查 `config.json` 路径是否正确
3. 路径中的 `\` 是否都改成了 `\\`

### 问题: 缺少主题
**解决**:
确保 `themes.py` 和 `open.exe` 在同一目录

---

## 📞 获取帮助

随时运行:
```cmd
open help
```

查看完整使用说明!

---

**享受高效的项目管理体验! 🎊**

