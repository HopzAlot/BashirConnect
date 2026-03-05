# 🧔🏽‍♂️📶 Meet Mr. Bashir: Your Personal Wi-Fi Connector

Tired of typing your credentials every single time you open your laptop or move between the hostel and the cafes? 

**Mr. Bashir** is a lightweight, invisible background utility designed to completely automate your Wi-Fi logins. His sole motive in life is to hunt down Fortinet captive portals (the system used across NUST networks) and log you in before you even open your browser. 

"Enter your login details once, JANAAAB!! WON'T ASK FOR THEM EVER AGAIN, I PROMISEE!!" — *Mr. Bashir*

## ✨ Features
* **Completely Invisible:** Runs silently in the Windows background with zero pop-ups.
* **Set It & Forget It:** Automatically adds himself to your Windows Startup folder.
* **Smart Detection:** Only activates when a Fortinet `fgtauth` captive portal intercepts your connection.
* **Battery Friendly:** Uses virtually zero CPU or RAM.

---

## 🚀 How to Set Up Mr. Bashir

You do **not** need Python installed. Just follow these steps:

1. Go to the **Releases** section on the right side of this page and download `nust_autologin.exe`.
2. Move the `.exe` file to your Desktop or Downloads folder and double-click it.
3. A black terminal window will pop up. Type your **Username** and **Password** and hit Enter. *(Note: Your password will be invisible while you type it—this is normal for security!)*
4. Mr. Bashir will securely save your details, copy himself to your Windows Startup folder, and then completely vanish.
5. **You're done!** From now on, whenever you boot up your laptop or connect to the campus network, he will handle the login instantly.

---

## 🔄 How to Reset Your Password

If you ever change your portal password, Mr. Bashir will be stuck trying to use the old one. To give him your new credentials:

1. Download the `Reset_Login.bat` file from this repository.
2. Double-click it.
3. This tool will safely stop Mr. Bashir in the background and delete your old saved password file.
4. Once it finishes, just double-click your main `nust_autologin.exe` file again to type in your new password.

---

## 🛑 How to Stop Mr. Bashir (Kill Switch)

Because Mr. Bashir is designed to be completely invisible, there is no physical "X" button to close him. If you ever need to manually stop him from running:

1. Press `Ctrl + Shift + Esc` to open **Task Manager**.
2. Click on the **Processes** or **Details** tab.
3. Scroll down until you find `nust_autologin.exe` (or `python.exe` if running from source).
4. Right-click it and select **End task**. 

*(Note: He will automatically wake up again the next time you restart your PC. To remove him permanently, delete `nust_autologin.exe` from your `shell:startup` folder).*