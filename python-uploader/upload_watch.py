#!/usr/bin/env python3
# Import required libraries
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from garmin_uploader.cli import upload_file

# Get output directory from environment or use default
WATCH_DIR = os.getenv("IC_OUTDIR", os.path.expanduser("~/activities"))

# Define class for file system event
class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith((".fit", ".tcx", ".gpx")):
            print(f"[WATCH] New activity found: {event.src_path}")
            # Call gupload for automatic upload
            upload_file([event.src_path], configfile=os.path.expanduser("~/.guploadrc"), activity_type="indoor_cycling")

if __name__ == "__main__":
    os.makedirs(WATCH_DIR, exist_ok=True)
    obs = Observer()
    obs.schedule(Handler(), WATCH_DIR, recursive=False)
    obs.start()
    print(f"[WATCH] Watching directory: {WATCH_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
