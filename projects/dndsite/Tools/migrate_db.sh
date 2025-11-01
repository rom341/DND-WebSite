#!/bin/bash
# migrate_db.sh

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
    echo "Error: Neither 'python3' nor 'python' command found. Please install Python to proceed."
    exit 1
fi

echo "🐍 Using Python command: $PYTHON_CMD"
echo "💾 Updating Django database..."

$PYTHON_CMD ../manage.py migrate

echo "✅ Database updated."