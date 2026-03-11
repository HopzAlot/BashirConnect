import time
import requests
import os
import sys
import json
import shutil
import getpass
import ctypes

# Paths for the Startup folder and credentials
STARTUP_DIR = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
CREDS_FILE = os.path.join(STARTUP_DIR, "wifi_creds.json")

def enforce_single_instance():
    """Prevents multiple copies of the script from running at the same time."""
    mutex_name = "NUST_Hostel_WiFi_Mutex_v1"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    
    if last_error == 183: # ERROR_ALREADY_EXISTS
        print("The auto-login script is already running in the background!")
        time.sleep(3)
        sys.exit(0)
    return mutex # Keep a reference to the mutex alive

def hide_console():
    """Hides the Windows command prompt window dynamically."""
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)

def install_to_startup():
    """Copies the executable to the Windows Startup folder."""
    if getattr(sys, 'frozen', False):
        current_exe = sys.executable
        exe_name = os.path.basename(current_exe)
        target_exe = os.path.join(STARTUP_DIR, exe_name)

        if current_exe.lower() != target_exe.lower():
            try:
                shutil.copy2(current_exe, target_exe)
                print("Successfully installed to Startup folder!")
            except Exception as e:
                print(f"Could not copy to startup: {e}")

def setup_credentials():
    """Prompts the user for credentials and saves them."""
    print("="*70)
    print("  Greetings from MR.BASHIR. I'm your personal hostel wifi connector...")
    print("="*70)
    print("No credentials found, JANAAAB!!. Please enter your login details. WON'T ASK FOR THEM EVER AGAIN, I PROMISEE!!")
    print("Enter your login details once. The script will run permanently")
    print("in the background and auto-login whenever needed.\n")
    
    username = input("Username: ")
    password = getpass.getpass("Password: ") 

    with open(CREDS_FILE, "w") as f:
        json.dump({"username": username, "password": password}, f)
    
    print("\nCredentials saved successfully! Hiding window and running in background...")
    time.sleep(3)

def get_credentials():
    """Loads credentials from the JSON file."""
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, "r") as f:
            creds = json.load(f)
            return creds.get("username"), creds.get("password")
    return None, None

def persistent_login_loop(username, password):
    """Continuously monitors network state and logs in when the portal appears."""
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
    # 1. Immediately check if another instance is already running
    mutex_reference = enforce_single_instance()
    
    # 2. Get saved credentials
    user, pwd = get_credentials()

    # 3. If first time running (no credentials found)
    if not user or not pwd:
        install_to_startup()
        setup_credentials()
        user, pwd = get_credentials()
        hide_console() # Hide terminal after they type their password
        persistent_login_loop(user, pwd)
        
    # 4. If running automatically on Startup (credentials exist)
    else:
        hide_console() # Hide terminal instantly
        persistent_login_loop(user, pwd)