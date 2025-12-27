from __future__ import annotations
import argparse
from pathlib import Path

DEFAULT_EXTS = [".flac", ".mp3", ".m4a", ".opus", ".ogg", ".wav", ".aac"]

def main() -> int:
    parser = argparse.ArgumentParser(description="generate minimal .m3u from files in current folder")
    parser.add_argument("--name", help="output m3u filename (default: <folder_name>.m3u)")
    parser.add_argument("--ext", action="append", help="include only these extensions (repeatable). ex: --ext .flac --ext .mp3")
    parser.add_argument("--no-sort", action="store_true", help="don't sort files (keep filesystem order)")
    args = parser.parse_args()
    
    folder = Path.cwd()
    exts = {(e if e.startswith(".") else f".{e}").lower() for e in (args.ext or DEFAULT_EXTS)}
    out_path = folder / (args.name or f"{folder.name}.m3u")
    
    # find and sort files
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts]
    if not args.no_sort:
        files.sort(key=lambda p: p.name.lower())
    
    # write m3u
    out_path.write_text("\n".join(p.name for p in files) + "\n", encoding="utf-8")
    
    print(f"generated: {out_path} ({len(files)} tracks)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())