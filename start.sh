#!/bin/bash
cd /app
echo "=== Files in /app ==="
ls -la
echo "=== Python files ==="
find /app -name "*.py" -type f

if [ -n "$BOT_FILE" ]; then
    echo "=== Running specified bot: $BOT_FILE ==="
    python "/app/$BOT_FILE"    exit $?
fi

if [ -f "/app/charlie_welcome_bot.py" ]; then
    echo "=== Running welcome bot ==="
    python /app/charlie_welcome_bot.py
else
    FILE=$(find /app -name "*.py" -type f | head -1)
    echo "=== Running: $FILE ==="
    python "$FILE"
fi
