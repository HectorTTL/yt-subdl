#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path
import glob
import shutil

def check_dependencies():
    for cmd in ["yt-dlp", "ffmpeg", "xclip"]:
        if not shutil.which(cmd):
            print(f"\u274c Missing dependency: {cmd}. Please install it.")
            sys.exit(1)

def get_clipboard_url():
    try:
        return subprocess.check_output("xclip -selection clipboard -o", shell=True).decode().strip()
    except Exception:
        print("\u274c Failed to get clipboard URL. Ensure xclip is installed or paste URL directly.")
        sys.exit(1)

def run_command(cmd):
    print(f"\n\u25b6 Running:\n{cmd}\n")
    subprocess.run(cmd, shell=True, check=True)

def main():
    check_dependencies()

    if len(sys.argv) < 2:
        print("Usage: ./videoscript.py <sub_lang> [--force-lang]")
        sys.exit(1)

    preferred_lang = sys.argv[1]
    force_lang = "--force-lang" in sys.argv
    url = get_clipboard_url()

    print(f"\ud83d\udccb Clipboard URL: {url}")
    print(f"\ud83c\udf10 Preferred subtitles: {preferred_lang}")
    if force_lang:
        print(f"\ud83d\udd12 Forced mode: only embed if subs match '{preferred_lang}'")

    download_dir = str(Path.home() / "Downloads")
    base_template = f"{download_dir}/%(title)s.%(ext)s"

    # Step 1: Download video + audio + auto subtitles
    dl_cmd = f"""
    yt-dlp -f "bv*+ba/b" --merge-output-format mp4 \
    --sub-lang "{preferred_lang}" --write-auto-sub --convert-subs srt \
    -o "{base_template}" "{url}"
    """
    run_command(dl_cmd.strip())

    # Step 2: Identify file components
    base_filename = subprocess.check_output(
        f'yt-dlp --get-filename -o "%(title)s" "{url}"',
        shell=True
    ).decode().strip()
    mp4_file = f"{download_dir}/{base_filename}.mp4"
    output_file = f"{download_dir}/{base_filename}.subtitled.mp4"

    # Step 3: Locate subtitle file
    srt_files = glob.glob(f"{download_dir}/{base_filename}.*.srt")
    if not Path(mp4_file).exists():
        print(f"\u274c ERROR: Video not found: {mp4_file}")
        sys.exit(1)
    if not srt_files:
        print("\u26a0\ufe0f No subtitles found. Skipping embedding.")
        print(f"\u2714\ufe0f Video is ready at: {mp4_file}")
        return

    srt_file = srt_files[0]
    actual_lang = srt_file.rsplit('.', 2)[-2]
    print(f"\ud83d\udcc4 Found subtitles: {os.path.basename(srt_file)} (lang: {actual_lang})")

    if force_lang and actual_lang != preferred_lang:
        print(f"\u26a0\ufe0f Subtitle language mismatch ({actual_lang} ≠ {preferred_lang}). Skipping embedding.")
        print(f"\u2714\ufe0f Video is ready at: {mp4_file}")
        return

    # Step 4: Burn subtitles
    burn_cmd = f"""
    ffmpeg -i "{mp4_file}" -sub_charenc UTF-8 \
    -vf "subtitles='{srt_file}'" -c:a copy "{output_file}"
    """
    run_command(burn_cmd.strip())

    # Step 5: Clean up
    try:
        os.remove(mp4_file)
        os.remove(srt_file)
        print(f"\ud83e\ude9f Cleaned up: {os.path.basename(mp4_file)} & {os.path.basename(srt_file)}")
    except Exception as e:
        print(f"\u26a0\ufe0f Cleanup failed: {e}")

    print(f"\n\u2705 Subtitled video created: {output_file}")

if __name__ == "__main__":
    main()

