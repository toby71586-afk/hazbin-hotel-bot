#!/bin/bash  
echo "=== Railway filesystem check ==="  
echo "PWD: $(pwd)"  
echo "--- Listing /app recursively ---"  
find /app -type f 2>/dev/null  
echo "--- done ---"  
