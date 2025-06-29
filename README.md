# yt-subdl 🎥

A simply effective script to download YouTube videos with embedded subtitles in your preferred language, designed originally for personal use & now made public for all who find it useful.

---

## ✨ Features

* Downloads MP4 video with audio
* Auto or preferred subtitle download (auto-generated subs via `yt-dlp`)
* Optionally *forces* a specific subtitle language
* Embeds subtitles directly into the video using `ffmpeg`
* Gets the video URL from your clipboard (via `xclip`)

---

## 🛠️ Requirements

* `yt-dlp`
* `ffmpeg`
* `xclip` (Linux clipboard tool — if you're not on Linux, adapt or replace)

Install via:

```bash
sudo apt install yt-dlp ffmpeg xclip
```

Make the script executable:

```bash
chmod +x videoscript.py
```

---

## 🚀 Usage

Copy a YouTube URL to your clipboard, then run:

```bash
./videoscript.py <sub_lang> [--force-lang]
```

Examples:

```bash
./videoscript.py en              # Tries to embed English subtitles
./videoscript.py fr --force-lang  # Only embeds if French subs are found
```

Outputs the final file to your Downloads folder as:

```
Video Title.subtitled.mp4
```

---

## 📄 LICENSE

This project is licensed under WTFPL.

Everyone is permitted to copy and distribute verbatim or modified copies of this license document,
and changing it is allowed as long as the name is changed.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE FUCK YOU WANT TO.

With one polite request: please credit the original author, Héctor Tormos, when redistributing or adapting the script.

---

## 👤 Author

**Héctor Tormos** — Linguist, script tamer, & accidental toolsmith.

---

Happy downloading ✨
