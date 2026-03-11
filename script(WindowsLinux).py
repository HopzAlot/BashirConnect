import time
import requests
import os
import sys
import json
import shutil
import getpass
import platform

# Detect the operating system
is_windows = platform.system() == "Windows"

# --- Cross-Platform Path Setup ---
if is_windows:
    STARTUP_DIR = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    CREDS_FILE = os.path.join(STARTUP_DIR, "wifi_creds.json")
else:
    # Linux standard hidden config directory
    CONFIG_DIR = os.path.expanduser("~/.config/mr_bashir")
    os.makedirs(CONFIG_DIR, exist_ok=True)
    CREDS_FILE = os.path.join(CONFIG_DIR, "wifi_creds.json")
    
    # Linux autostart directory
    AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
    os.makedirs(AUTOSTART_DIR, exist_ok=True)

def enforce_single_instance():
    """Cross-platform check to prevent multiple instances."""
    if is_windows:
        import ctypes
        mutex_name = "NUST_Hostel_WiFi_Mutex_v1"
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
        if ctypes.windll.kernel32.GetLastError() == 183: # ERROR_ALREADY_EXISTS
            print("Mr. Bashir is already running in the background!")
            time.sleep(3)
            sys.exit(0)
        return mutex
    else:
        # We import fcntl here so Windows doesn't crash trying to find a Linux-only module
        import fcntl
        lock_file = "/tmp/mr_bashir.lock"
        lock_file_pointer = open(lock_file, 'w')
        try:
            # Try to get an exclusive, non-blocking lock on the file
            fcntl.lockf(lock_file_pointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lock_file_pointer
        except BlockingIOError:
            print("Mr. Bashir is already running in the background!")
            sys.exit(0)

def hide_console():
    """Hides the console on Windows. Linux handles this natively via the .desktop file."""
    if is_windows:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)

def install_to_startup():
    """Installs to the appropriate OS startup location."""
    if getattr(sys, 'frozen', False):
        current_path = sys.executable
    else:
        current_path = os.path.abspath(sys.argv[0])

    if is_windows:
        exe_name = os.path.basename(current_path)
        target_path = os.path.join(STARTUP_DIR, exe_name)
        if current_path.lower() != target_path.lower():
            try:
                shutil.copy2(current_path, target_path)
                print("Successfully installed to Windows Startup folder!")
            except Exception as e:
                print(f"Could not copy to startup: {e}")
    else:
        # Linux Autostart setup
        desktop_file_path = os.path.join(AUTOSTART_DIR, "mr_bashir.desktop")
        desktop_content = f"""[Desktop Entry]
Type=Application
Exec={current_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Mr. Bashir Wi-Fi Connector
Comment=Automatically logs into the Fortinet portal
Terminal=false
"""
        try:
            with open(desktop_file_path, 'w') as f:
                f.write(desktop_content)
            
            # Make the Linux script executable just in case
            os.chmod(current_path, 0o755) 
            print("Successfully added to Linux autostart!")
        except Exception as e:
            print(f"Could not add to autostart: {e}")

def setup_credentials():
    print("="*45)
    print("   Greetings from MR.BASHIR. I'm your personal Wi-Fi connector...")
    print("="*45)
    print("No credentials found, JANAAAB!!. Please enter your login details.")
    print("WON'T ASK FOR THEM EVER AGAIN, I PROMISEE!!\n")
    
    username = input("Username: ")
    password = getpass.getpass("Password: ") 

    with open(CREDS_FILE, "w") as f:
        json.dump({"username": username, "password": password}, f)
    
    print("\nCredentials saved successfully! Running in background...")
    time.sleep(3)

def get_credentials():
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, "r") as f:
            creds = json.load(f)
            return creds.get("username"), creds.get("password")
    return None, None

def persistent_login_loop(username, password):
    session = requests.Session()
    
    while True:
        try:
            response = session.get("http://neverssl.com", timeout=5)
            
            if "fgtauth" in response.url:
                dynamic_login_url = response.url
                magic_token = dynamic_login_url.split('?')[-1]
                
                payload = {
                    "username": username,
                    "password": password,
                    "magic": magic_token
                }
                
                base_post_url = dynamic_login_url.split('fgtauth')[0]
                session.post(base_post_url, data=payload, timeout=10)
                
                time.sleep(10) 
                continue 
            
            elif "neverssl.com" in response.url:
                time.sleep(60)
                
        except requests.exceptions.RequestException:
            time.sleep(10)

if __name__ == "__main__":
    # 1. Check if another instance is running (Cross-platform)
    lock_reference = enforce_single_instance()
    
    # 2. Get saved credentials
    user, pwd = get_credentials()

    # 3. First time running
    if not user or not pwd:
        install_to_startup()
        setup_credentials()
        user, pwd = get_credentials()
        hide_console() 
        persistent_login_loop(user, pwd)
        
    # 4. Running automatically on Startup
    else:
        hide_console() 
        persistent_login_loop(user, pwd)