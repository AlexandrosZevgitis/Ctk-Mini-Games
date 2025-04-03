import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.start_script()

    def start_script(self):
        if self.process:
            self.process.kill()  # Kill previous process
        self.process = subprocess.Popen(["python", self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Only restart on .py file changes
            print(f"🔄 Reloading {self.script_name} due to changes...")
            self.start_script()

def watch(script_name):
    event_handler = ReloadHandler(script_name)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    watch("Login_GUI.py")  # Replace with your main Python script
