#!/bin/sh

# Claude Code 便携启动入口（无需系统 Python）

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
SYSTEM_NAME="$(uname -s)"

case "$SYSTEM_NAME" in
    Darwin*)
        PYTHON_EXE="$SCRIPT_DIR/venv_mac/bin/python"
        ;;
    Linux*)
        PYTHON_EXE="$SCRIPT_DIR/venv_linux/bin/python"
        ;;
    *)
        echo "❌ 不支持的系统：$SYSTEM_NAME"
        exit 1
        ;;
esac

if [ ! -x "$PYTHON_EXE" ]; then
    echo "❌ 未找到对应虚拟环境：$PYTHON_EXE"
    echo
    echo "请先在当前目录构建当前系统的虚拟环境："
    echo "   python3 build_venv.py"
    exit 1
fi

exec "$PYTHON_EXE" "$SCRIPT_DIR/run.py" "$@"