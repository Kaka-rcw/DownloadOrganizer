from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
SUFFIX_MAP = {
    "images": [".jpg", ".png", ".svg", ".gif"],
    "videos": [".mp4", ".mov", ".avi", ".wmv", ".mkv"],
    "textFiles": [".doc", ".txt", ".md", ".log", ".csv", ".json", ".xml"],
    "books": [".epub", ".mobi"],
    "compressedFiles": [".zip", ".rar", ".7z", ".gz", ".tar.gz"],
    "audio": [".mp3", ".wav", ".aiff", ".wma", ".aac", ".flac", ".ogg"],
    "pdf": [".pdf"],
    "code": [".py", ".c", ".cpp", ".js", ".ts", ".html", ".css"]
}
p = Path("~/Downloads").expanduser()

def main():
    watchFileChange(p)

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            handleFile(p)

def handleFile(p):
    for file in p.glob("*"):
        if not file.is_file():
            continue
        et = file.suffix.lower()
        for category, suffix in SUFFIX_MAP.items():
            if et in suffix:
                process(file, category)
                break
        else:
            process(file, "etc")

def process(file, tp):
    des_dir = Path(f"~/Downloads/{tp}/").expanduser()
    des = des_dir / file.name
    des.parent.mkdir(parents=True, exist_ok=True)
    index = 1
    while des.exists():
        des = des_dir /f"{des.stem}_{index}{des.suffix}"
        index += 1
    file.rename(des)

def watchFileChange(p):
    handler = NewFileHandler()
    observer = Observer()
    observer.schedule(handler, p, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()