import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from batch_ingest import ingest_from_file

class WatchHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".txt"):
            print(f"Detected new file: {event.src_path}")
            ingest_from_file(event.src_path)

if __name__ == "__main__":
    folder = "watched/"
    observer = Observer()
    observer.schedule(WatchHandler(), folder, recursive=False)
    observer.start()
    print(f"Watching folder: {folder}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
