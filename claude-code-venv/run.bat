@echo off
setlocal

REM Claude Code 便携启动入口（无需系统 Python）
set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=%SCRIPT_DIR%venv_win\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo ❌ 未找到 Windows 虚拟环境：%PYTHON_EXE%
    echo.
    echo 请先在当前目录构建 Windows 虚拟环境：
    echo    python build_venv.py --win
    exit /b 1
)

"%PYTHON_EXE%" "%SCRIPT_DIR%run.py" %*
exit /b %ERRORLEVEL%