@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║              🧪 测试运行 - 无需安装                       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo 💡 这个脚本可以在不安装的情况下测试程序
echo    适合在部署到新电脑前先测试功能
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM 获取当前目录
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

REM 临时添加到PATH
set PATH=%PATH%;%CURRENT_DIR%

echo ✅ 已临时添加到PATH
echo 📂 当前目录: %CURRENT_DIR%
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🎮 现在可以测试以下命令:
echo.
echo    open           启动主菜单
echo    open help      查看帮助
echo    open add       添加项目
echo    open ls        批量打开项目
echo    open rm        批量删除项目
echo    open style     切换主题
echo    open stats     查看统计
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 💡 输入命令测试,输入 exit 退出
echo.

REM 启动交互式CMD
cmd /k

