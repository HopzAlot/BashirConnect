#!/bin/bash

echo "============================================="
echo "   Mr. Bashir - Credential Reset Utility"
echo "============================================="

# 1. Kill any running instances of Mr. Bashir
echo "[*] Asking Mr. Bashir to step down..."
pkill -f "script.py" > /dev/null 2>&1
pkill -f "script(WindowsLinux).py" > /dev/null 2>&1
pkill -f "mr_bashir.py" > /dev/null 2>&1

# 2. Define the path to the hidden config folder
CONFIG_DIR="$HOME/.config/mr_bashir"
CREDS_FILE="$CONFIG_DIR/wifi_creds.json"
LOCK_FILE="$CONFIG_DIR/mr_bashir.lock"

# 3. Delete the credentials file
if [ -f "$CREDS_FILE" ]; then
    rm "$CREDS_FILE"
    echo "[*] Memory wiped! Old credentials deleted, JANAAAB!"
else
    echo "[*] No saved credentials found. You are already starting fresh."
fi

# 4. Clean up the lock file so the next run is guaranteed to work
if [ -f "$LOCK_FILE" ]; then
    rm "$LOCK_FILE"
    echo "[*] Lock file cleared."
fi

echo ""
echo "Done! Run your Python script again to enter your new NUST password."
echo "============================================="