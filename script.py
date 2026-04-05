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

# Detect if running specifically inside Termux on Android
is_termux = "com.termux" in os.environ.get("PREFIX", "")

# --- Cross-Platform Path Setup ---
if is_windows:
    STARTUP_DIR = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    CONFIG_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'MrBashir')
    os.makedirs(CONFIG_DIR, exist_ok=True)
    CREDS_FILE = os.path.join(CONFIG_DIR, "wifi_creds.json")
else:
    # Linux / Termux standard hidden config directory
    CONFIG_DIR = os.path.expanduser("~/.config/mr_bashir")
    os.makedirs(CONFIG_DIR, exist_ok=True)
    CREDS_FILE = os.path.join(CONFIG_DIR, "wifi_creds.json")
    
    # Desktop Linux autostart directory (Ignored by Termux)
    if not is_termux:
        AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
        os.makedirs(AUTOSTART_DIR, exist_ok=True)

def enforce_single_instance():
    if is_windows:
        import ctypes
        mutex_name = "NUST_Hostel_WiFi_Mutex_v1"
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
        if ctypes.windll.kernel32.GetLastError() == 183:
            print("Mr. Bashir is already running in the background!")
            time.sleep(3)
            sys.exit(0)
        return mutex
    else:
        import fcntl
        lock_file = os.path.join(CONFIG_DIR, "mr_bashir.lock")
        lock_file_pointer = open(lock_file, 'w')
        try:
            fcntl.lockf(lock_file_pointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return lock_file_pointer
        except BlockingIOError:
            print("Mr. Bashir is already running in the background!")
            sys.exit(0)

def hide_console():
    if is_windows:
        import ctypes
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)

def install_to_startup():
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
    elif not is_termux:
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
            os.chmod(current_path, 0o755) 
            print("Successfully added to Linux autostart!")
        except Exception as e:
            print(f"Could not add to autostart: {e}")

def setup_credentials():
    print("="*45)
    print("   Greetings from MR.BASHIR. I'm your personal Wi-Fi connector...")
    print("="*45)
    print("No credentials found, JANAAAB!!. Please enter your login details.\n")
    
    username = input("Username: ")
    password = getpass.getpass("Password: ") 

    with open(CREDS_FILE, "w") as f:
        json.dump({"username": username, "password": password}, f)
    
    print("\nCredentials saved successfully!")
    time.sleep(2)

def get_credentials():
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, "r") as f:
            creds = json.load(f)
            return creds.get("username"), creds.get("password")
    return None, None

def persistent_login_loop(username, password):
    session = requests.Session()
    print("\n[*] Mr. Bashir is awake. Starting the network monitoring loop...")
    print("\n[*] Pinging 1.1.1.1 to check connection status...")
    while True:
        try:
            # Using 30 seconds here to account for slow hostel Wi-Fi
            response = session.get("http://1.1.1.1", timeout=30)
                        
            if "fgtauth" in response.url:
                print("[!] Captive portal detected! Extracting magic token...")
                dynamic_login_url = response.url
                magic_token = dynamic_login_url.split('?')[-1]
                
                payload = {
                    "username": username,
                    "password": password,
                    "magic": magic_token
                }
                
                base_post_url = dynamic_login_url.split('fgtauth')[0]
                print(f"[*] Sending credentials to: {base_post_url}")
                res = session.post(base_post_url, data=payload, timeout=10)
                print(f"[*] Login POST request finished with status code: {res.status_code}")
                
                time.sleep(10) 
                continue 
            
            elif "neverssl.com" in response.url:
                print("[*] Internet is working perfectly. Going to sleep for 60 seconds...")
                time.sleep(60)
                
        except requests.exceptions.RequestException as e:
            print(f"[X] Network request failed (Wi-Fi might be off or Android is blocking it): {e}")
            time.sleep(10)

if __name__ == "__main__":
    if is_termux:
        print("[*] Termux detected! Acquiring wake-lock to prevent Android battery manager from killing the script...")
        os.system("termux-wake-lock")

    lock_reference = enforce_single_instance()
    user, pwd = get_credentials()

    if not user or not pwd:
        install_to_startup()
        setup_credentials()
        user, pwd = get_credentials()
        hide_console() 
        persistent_login_loop(user, pwd)
    else:
        hide_console() 
        persistent_login_loop(user, pwd)
