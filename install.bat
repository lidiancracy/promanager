@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║         🚀 项目启动器 - 安装脚本                       ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM 获取当前脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo 📂 安装路径: %SCRIPT_DIR%
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 💡 请先安装 Python: https://www.python.org/
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.

REM 安装必需依赖
echo 📦 正在安装必需依赖...
pip install inquirer prompt_toolkit
echo.

REM 检查是否已在 PATH 中
echo %PATH% | findstr /C:"%SCRIPT_DIR%" >nul
if errorlevel 1 (
    echo.
    echo ⚙️  添加到系统 PATH...
    echo.
    echo 方式 1: 临时添加 (仅当前 CMD 会话有效)
    echo    运行: set PATH=%%PATH%%;%SCRIPT_DIR%
    echo.
    echo 方式 2: 永久添加 (推荐)
    echo    需要管理员权限,是否现在添加?
    echo.
    set /p ADD_PATH="永久添加到 PATH? (Y/n): "
    
    if /i "%ADD_PATH%"=="y" (
        setx PATH "%PATH%;%SCRIPT_DIR%"
        echo ✅ 已添加到 PATH
        echo 💡 请重新打开 CMD 窗口使其生效
    ) else if "%ADD_PATH%"=="" (
        setx PATH "%PATH%;%SCRIPT_DIR%"
        echo ✅ 已添加到 PATH
        echo 💡 请重新打开 CMD 窗口使其生效
    ) else (
        echo.
        echo 手动添加方法:
        echo 1. 右键 "此电脑" - 属性
        echo 2. 高级系统设置 - 环境变量
        echo 3. 在 "用户变量" 或 "系统变量" 中找到 Path
        echo 4. 添加: %SCRIPT_DIR%
    )
) else (
    echo ✅ 已在 PATH 中
)

echo.
echo ═══════════════════════════════════════════════════════════
echo ✅ 安装完成!
echo.
echo 📖 快速开始:
echo    open           - 显示项目列表
echo    open help      - 查看帮助
echo    open add       - 添加当前目录为项目
echo.
echo 💡 提示: 如果是首次安装,请重新打开 CMD 窗口
echo ═══════════════════════════════════════════════════════════
echo.
pause

