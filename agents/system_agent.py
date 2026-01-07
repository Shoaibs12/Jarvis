import os
import subprocess
import webbrowser
import ctypes
from pathlib import Path
import urllib.parse

class SystemAgent:

    # ------------------------------------------------------
    # OPEN APPLICATIONS
    # ------------------------------------------------------
    def open_app(self, query):
        q = query.lower()

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

    # ------------------------------------------------------
    # OPEN WEBSITE
    # ------------------------------------------------------
    def open_website(self, query):
        q = query.lower()

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

        return None  # allow fallback

    # ------------------------------------------------------
    # SEARCH INSIDE CHROME
    # ------------------------------------------------------
    def chrome_search(self, query):
        """
        Opens Chrome with a Google search.
        """
        search_query = query.lower().replace("search", "").strip()
        if not search_query:
            return "What should I search for, sir?"

        encoded = urllib.parse.quote(search_query)
        url = f"https://www.google.com/search?q={encoded}"

        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        try:
            subprocess.Popen([chrome_path, url])
            return f"Searching for '{search_query}' in Chrome, sir."
        except:
            webbrowser.open(url)
            return f"Searching for '{search_query}', sir."

    # ------------------------------------------------------
    # VOLUME CONTROL
    # ------------------------------------------------------
    def control_volume(self, query):
        q = query.lower()

        if "increase" in q or "up" in q:
            for _ in range(5):
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            return "Increasing volume."

        if "decrease" in q or "down" in q:
            for _ in range(5):
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            return "Decreasing volume."

        if "mute" in q:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            return "Muting volume."

        if "unmute" in q:
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            return "Unmuting volume."

        return "I couldn't understand the volume command."

    # ------------------------------------------------------
    # POWER CONTROLS
    # ------------------------------------------------------
    def shutdown(self):
        os.system("shutdown /s /t 1")
        return "Shutting down, sir."

    def restart(self):
        os.system("shutdown /r /t 1")
        return "Restarting system, sir."

    def sleep(self):
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting the system to sleep, sir."

    # ------------------------------------------------------
    # OPEN FOLDERS
    # ------------------------------------------------------
    def open_folder(self, query):
        q = query.lower()

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

    # ------------------------------------------------------
    # MASTER HANDLER
    # ------------------------------------------------------
    def handle(self, query):
        q = query.lower()

        if "search" in q:
            return self.chrome_search(q)

        if "open" in q:
            # Try app
            resp = self.open_app(q)
            if "Opening" in resp:
                return resp

            # Try website
            resp = self.open_website(q)
            if resp:
                return resp

            return "I couldn't open what you asked for, sir."

        if "volume" in q or "mute" in q:
            return self.control_volume(q)

        if "shutdown" in q:
            return self.shutdown()

        if "restart" in q:
            return self.restart()

        if "sleep" in q:
            return self.sleep()

        if "folder" in q or "downloads" in q or "documents" in q or "desktop" in q:
            return self.open_folder(q)

        return "System action not recognized, sir."
