#!/bin/bash  
cd /app  
echo "=== Files in /app ==="  
ls -la  
echo "=== Searching deeper ==="  
find /app -name "*.py" -type f  
echo "=== Running first .py found ==="  
FILE=$(find /app -name "charlie_welcome_bot.py" -o -name "charlie_welcome_bot*.py" | head -1)  
echo "Found: $FILE"  
python "$FILE"  
