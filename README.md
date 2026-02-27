# 🦆 nestscan — Pretty Directory Trees in One Command

> *"Because sometimes you just need to see what's actually in a folder without losing your mind."*

---

## 🚀 Install

```bash
pip install nestscan
```

---

## ⚡ Usage

Navigate to any folder and run:

```bash
nestscan
```

It prints a clean, readable tree of your current directory — sorted, structured, color-coded, and easy on the eyes.

You can also point it anywhere:

```bash
nestscan /path/to/my/project
```

---

## 🛠 All Options

| Flag | Description |
|------|-------------|
| `path` | Target directory to scan (default: current directory) |
| `-o`, `--output` | Save the tree to a text file (e.g., `-o tree.txt`) — ANSI colors are automatically stripped for clean output |
| `--all` | Include hidden/junk directories like `.git`, `node_modules`, `venv`, etc. |
| `--stats` | Show file sizes next to every file |
| `--llm` | Format output for pasting directly into an LLM prompt (wraps in a code block, skips the banner) |

### Examples

```bash
# Scan the current directory
nestscan

# Scan a specific path
nestscan /home/user/myproject

# Save output to a clean text file
nestscan -o tree.txt

# Show file sizes
nestscan --stats

# Include hidden and junk folders
nestscan --all

# Copy-paste ready output for ChatGPT, Claude, etc.
nestscan --llm

# Combine flags
nestscan /home/user/myproject --stats --all -o full_tree.txt
```

---

## 📋 Example Output

```
Directory Tree for: /home/user/myproject
==================================================
myproject/
├── src/
│   ├── main.py              [  4.2KB]
│   ├── utils.py             [  1.8KB]
│   └── models/
│       ├── user.py          [  2.1KB]
│       └── post.py          [  1.3KB]
├── tests/
│   ├── test_main.py         [  3.0KB]
│   └── test_utils.py        [  1.1KB]
├── README.md                [  2.4KB]
└── requirements.txt         [    89B]
```

Clean. Sorted. Directories first. Color-coded by file type.

---

## 🎨 Color Coding

| Color | File Types |
|-------|-----------|
| 🟡 Yellow | `.py`, `.pyc`, `.pyw` |
| 🟢 Green | `.md`, `.txt`, `.csv`, `.log` |
| 🟣 Magenta | `.json`, `.toml`, `.yaml`, `.yml`, `.ini`, `.cfg` |
| 🔴 Red | `.sh`, `.bat`, `.exe`, `.dll`, `.so` |
| Bold Cyan | Directories |

---

## ✨ What It Does

- 🌲 **Recursive tree generation** — walks the full directory structure with proper branch characters
- 🎨 **Color-coded by file type** — instantly see what kind of files you're dealing with
- 📁 **Directories first** — folders always listed before files at every level
- 🚫 **Respects `.gitignore`** — automatically reads your `.gitignore` and skips what it says, plus a built-in fallback list of common junk folders
- 📊 **Optional file sizes** — `--stats` shows human-readable sizes (`KB`, `MB`, etc.) next to each file
- 🤖 **LLM mode** — `--llm` wraps the output in a code block and skips the banner so you can paste your project structure straight into an AI prompt without any cleanup
- 💾 **Clean file output** — when saving with `-o`, ANSI color codes are automatically stripped so your text file is actually readable
- 🪟 **Windows compatible** — ANSI colors work there too

---

## 🛠 Requirements

- Python 3.6+
- No third-party dependencies — pure stdlib, zero bloat

---

## ⚠️ Notes

- Directories you don't have permission to read will show `[Permission Denied]` instead of crashing
- `.gitignore` is parsed from the root of the scanned directory — nested `.gitignore` files are not currently supported
- Output is sorted alphabetically within each level, with directories always above files

---

## 🤝 Contributing

Found a bug? Have a wild idea? PRs welcome.

---

## 📜 License

Do whatever you want with it. Just stop doing `ls -la` and squinting at terminal output like it's 1995.

---

*By turnt ducky 🦆 — also check out [reqscan](https://github.com/turntducky/reqscan) for auto-generating `requirements.txt`.*
