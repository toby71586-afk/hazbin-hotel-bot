#!/bin/bash  
# Force Railway to find and run the bot  
cd /app || exit 1  
echo "Current directory: $(pwd)"  
echo "Files in this directory:"  
ls -la

# Run the bot  
python charlie_welcome_bot.py
