from pathlib import Path

SUFFIX_MAP = {
    "images": [".jpg", ".png", ".svg", ".gif"],
    "videos": [".mp4", ".mov", ".avi", ".wmv", ".mkv"],
    "textFiles": [".doc", ".txt", ".md", ".log", ".csv", ".json", ".xml"],
    "books": [".epub", ".mobi"],
    "compressedFiles": [".zip", ".rar", ".7z", ".gz", ".tar.gz"],
    "audio": [".mp3", ".wav", ".aiff", ".wma", ".aac", ".flac", ".ogg"],
    "pdf": [".pdf"],
}

def main():
    p = Path("~/dev/test-project").expanduser()
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
    des_dir = Path(f"~/dev/test-project/{tp}/").expanduser()
    des = des_dir / file.name
    des.parent.mkdir(parents=True, exist_ok=True)
    file.rename(des)

if __name__ == "__main__":
    main()