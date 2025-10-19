@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║            🚀 项目启动器 - 一键安装                       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM 获取当前脚本所在目录
set "INSTALL_DIR=%~dp0"
set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"

echo 📂 安装位置: %INSTALL_DIR%
echo.

REM 检查 open.exe 是否存在
if not exist "%INSTALL_DIR%\open.exe" (
    echo ❌ 错误: 找不到 open.exe
    echo 💡 请确保 open.exe 和本脚本在同一目录
    pause
    exit /b 1
)

echo ✅ 找到程序文件
echo.

REM 检查 config.json 是否存在
if not exist "%INSTALL_DIR%\config.json" (
    echo ⚠️  警告: 未找到 config.json
    if exist "%INSTALL_DIR%\config.example.json" (
        echo 💡 正在复制示例配置...
        copy "%INSTALL_DIR%\config.example.json" "%INSTALL_DIR%\config.json" >nul
        echo ✅ 已创建 config.json
        echo.
        echo ⚙️  请编辑 config.json 配置你的 IDE 路径!
        echo.
    ) else (
        echo ⚠️  将使用内置默认配置
        echo.
    )
) else (
    echo ✅ 找到配置文件
    echo.
)

REM 检查是否已在 PATH 中
echo %PATH% | findstr /C:"%INSTALL_DIR%" >nul
if errorlevel 1 (
    echo 📝 添加到系统 PATH...
    echo.
    
    setx PATH "%PATH%;%INSTALL_DIR%" >nul 2>&1
    
    if errorlevel 1 (
        echo ❌ 添加失败,可能需要管理员权限
        echo.
        echo 💡 手动添加方法:
        echo    1. 右键"此电脑" - 属性
        echo    2. 高级系统设置 - 环境变量
        echo    3. 在 Path 中添加: %INSTALL_DIR%
        echo.
    ) else (
        echo ✅ 已添加到 PATH
        echo.
    )
) else (
    echo ✅ 已在 PATH 中
    echo.
)

echo ─────────────────────────────────────────────────────────────
echo ✅ 安装完成!
echo ─────────────────────────────────────────────────────────────
echo.
echo 📝 下一步:
echo.
echo   1. ⚙️  编辑 config.json 配置 IDE 路径 (重要!)
echo   2. 🔄 重新打开 CMD 窗口
echo   3. 🚀 输入 open 开始使用
echo.
echo 💡 快速开始:
echo   • open add      添加项目
echo   • open list     查看项目
echo   • open help     查看帮助
echo.
echo ─────────────────────────────────────────────────────────────
echo.

REM 询问是否立即编辑配置
set /p EDIT_CONFIG="是否现在编辑 config.json? (Y/n): "

if /i "%EDIT_CONFIG%"=="y" (
    notepad "%INSTALL_DIR%\config.json"
) else if "%EDIT_CONFIG%"=="" (
    notepad "%INSTALL_DIR%\config.json"
)

echo.
pause

