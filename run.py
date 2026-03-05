import time
import requests
import os
import json
import sys
import getpass

# Build an absolute path to store the credentials right next to the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(SCRIPT_DIR, "wifi_creds.json")

def get_credentials():
    """Loads saved credentials, or prompts the user if they don't exist."""
    
    # Check if the user passed the '--reset' flag to change credentials
    if "--reset" in sys.argv:
        if os.path.exists(CREDS_FILE):
            os.remove(CREDS_FILE)
            print("Old credentials removed.")

    # Load from file if it exists
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, "r") as f:
            creds = json.load(f)
            # Just a quick printout so you know how to change them if watching the terminal
            print(f"Loaded saved credentials for '{creds.get('username')}'.")
            print(f"To change credentials, run: python {os.path.basename(__file__)} --reset\n")
            return creds.get("username"), creds.get("password")

    # If no file exists, prompt the user in the terminal
    print("\n" + "="*40)
    print("   Greetings from MR.BASHIR. I'm your personal hostel wifi connector...")
    print("="*40)
    print("No credentials found, JANAAAB!!. Please enter your login details. WON'T ASK FOR THEM EVER AGAIN, I PROMISEE!!")
    print("These will be saved locally so you don't have to enter them again, JANAAB!!")
    
    username = input("Username: ")
    # getpass hides the text while typing, just like a Linux terminal
    password = getpass.getpass("Password: ") 

    # Save to the JSON file for next time
    with open(CREDS_FILE, "w") as f:
        json.dump({"username": username, "password": password}, f)
    
    print("\nCredentials saved successfully!")
    print(f"To change them later, just run this script with the --reset flag:")
    print(f"python {os.path.basename(__file__)} --reset")
    print("="*40 + "\n")
    
    return username, password

def wait_and_login(username, password):
    session = requests.Session()
    print("Waiting for Wi-Fi connection...")

    while True:
        try:
            # 1. Trigger the portal intercept
            response = session.get("http://neverssl.com", timeout=5)
            
        except requests.exceptions.RequestException:
            print("Wi-Fi not connected yet. Retrying in 3 seconds...")
            time.sleep(3)
            continue # Skip the rest of the loop and try again

        # 2. Check if we hit the Fortinet portal
        if "fgtauth" in response.url:
            dynamic_login_url = response.url
            print(f"Fortinet portal detected at: {dynamic_login_url}")
            
            # Extract the "magic" token from the end of the URL
            magic_token = dynamic_login_url.split('?')[-1]
            
            # 3. Prepare the Fortinet-specific payload
            payload = {
                "username": username,
                "password": password,
                "magic": magic_token
            }
            
            # Fortinet usually expects the POST request to go to the base URL
            base_post_url = dynamic_login_url.split('fgtauth')[0]
            
            print(f"Sending login credentials to {base_post_url}...")
            
            try:
                login_response = session.post(base_post_url, data=payload, timeout=10)
                
                # Check if it was successful 
                if login_response.status_code == 200:
                    print("Login successful! You should have internet access now.")
                else:
                    print(f"Login failed. Server returned status code: {login_response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"The router dropped the POST request: {e}")
            
            break # Exit loop after attempting login
            
        elif "neverssl.com" in response.url:
            print("No portal detected. You already have internet access!")
            break
        else:
            print(f"Unknown portal detected: {response.url}")
            break

if __name__ == "__main__":
    # Fetch credentials first, then pass them to the login function
    user, pwd = get_credentials()
    wait_and_login(user, pwd)