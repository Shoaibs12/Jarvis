import os
import subprocess
import webbrowser
import ctypes
from pathlib import Path
import urllib.parse

def open_application(app_name: str) -> str:
    """
    Opens a desktop application by name. Supported apps: chrome, vs code, code, notepad, calculator, paint, cmd.

    Args:
        app_name: The name of the application to open.
    """
    q = app_name.lower()
    apps = {
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vs code": r"C:\Users\LENOVO\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "code": r"C:\Users\LENOVO\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
    }

    for app, path in apps.items():
        if app in q:
            try:
                subprocess.Popen(path)
                return f"Opening {app}, sir."
            except Exception as e:
                return f"Unable to open {app}: {e}"
    return "I couldn't find that application, sir."

def open_website(url_name: str) -> str:
    """
    Opens a common website. Supported sites: youtube, google, gmail, whatsapp, github.

    Args:
        url_name: The name of the website to open.
    """
    q = url_name.lower()
    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "gmail": "https://mail.google.com",
        "whatsapp": "https://web.whatsapp.com",
        "github": "https://github.com",
    }

    for name, url in sites.items():
        if name in q:
            webbrowser.open(url)
            return f"Opening {name}, sir."
    return "I couldn't find that website, sir."

def chrome_search(search_query: str) -> str:
    """
    Opens Chrome and performs a Google search for the specified query.

    Args:
        search_query: The term or phrase to search for.
    """
    if not search_query:
        return "What should I search for, sir?"
    encoded = urllib.parse.quote(search_query)
    url = f"https://www.google.com/search?q={encoded}"
    try:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([chrome_path, url])
        return f"Searching for '{search_query}' in Chrome, sir."
    except:
        webbrowser.open(url)
        return f"Searching for '{search_query}', sir."

def control_volume(action: str) -> str:
    """
    Controls the system volume.

    Args:
        action: The volume action to take. Should be 'increase', 'decrease', 'mute', or 'unmute'.
    """
    q = action.lower()
    if "increase" in q or "up" in q:
        for _ in range(5):
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
        return "Increasing volume."
    if "decrease" in q or "down" in q:
        for _ in range(5):
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
        return "Decreasing volume."
    if "mute" in q or "unmute" in q:
        ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
        return "Toggling mute."
    return "I couldn't understand the volume command."

def power_control(action: str) -> str:
    """
    Controls the system power.

    Args:
        action: The power action to take. Should be 'shutdown', 'restart', or 'sleep'.
    """
    q = action.lower()
    if "shutdown" in q:
        os.system("shutdown /s /t 1")
        return "Shutting down, sir."
    if "restart" in q:
        os.system("shutdown /r /t 1")
        return "Restarting system, sir."
    if "sleep" in q:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting the system to sleep, sir."
    return "Power action not recognized."

def open_folder(folder_name: str) -> str:
    """
    Opens a standard system folder.

    Args:
        folder_name: The folder to open. Should be 'downloads', 'documents', or 'desktop'.
    """
    q = folder_name.lower()
    folders = {
        "downloads": str(Path.home() / "Downloads"),
        "documents": str(Path.home() / "Documents"),
        "desktop": str(Path.home() / "Desktop"),
    }
    for name, path in folders.items():
        if name in q:
            subprocess.Popen(f'explorer "{path}"')
            return f"Opening {name} folder."
    return "Folder not recognized, sir."
