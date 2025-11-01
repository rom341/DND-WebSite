#!/bin/bash
# run_server.sh

find_python_command() {
    if command -v python3 &> /dev/null; then
        echo "python3"
    elif command -v python &> /dev/null; then
        echo "python"
    else
        echo ""
    fi
}

PYTHON_CMD=$(find_python_command)

if [ -z "$PYTHON_CMD" ]; then
    echo "ERROR: Neither 'python3' nor 'python' command found. Please install Python to proceed."
    exit 1
fi

echo "🐍 Using Python command: $PYTHON_CMD"
echo "🚀 Starting Django development server (http://127.0.0.1:8000/)..."

$PYTHON_CMD ../manage.py runserver

# The server will run until you press Ctrl+C