#!/bin/sh
# Docker entrypoint script for Railway

echo "========================================="
echo "🚀 Starting Eye of Horus on Railway"
echo "========================================="

# Wait for old instance to fully terminate
echo "⏳ Waiting 5 seconds for clean start..."
sleep 5

# Start the bot
python main.py
