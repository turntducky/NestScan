import os
import sys
import argparse
import fnmatch
import re
from pathlib import Path

if os.name == 'nt':
    os.system("")

class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

SKIP_DIRS = {
    ".git", "venv", ".venv", "env", ".env", "envs", "node_modules", 
    "__pycache__", "build", "dist", ".idea", ".vscode", "site-packages"
}

def print_banner():
    banner = fr"""{C.CYAN}{C.BOLD}
  _   _           _    _____                 
 | \ | |         | |  / ____|                
 |  \| | ___  ___| |_| (___   ___ __ _ _ __  
 | . ` |/ _ \/ __| __|\___ \ / __/ _` | '_ \ 
 | |\  |  __/\__ \ |_ ____) | (_| (_| | | | |
 |_| \_|\___||___/\__|_____/ \___\__,_|_| |_|   
                                          
 | Developed by : turnt ducky 🦆 |{C.RESET}"""
    print(banner)

def parse_gitignore(root_path: Path) -> list:
    """Extracts ignored patterns from a .gitignore file if it exists."""
    ignore_patterns = list(SKIP_DIRS)
    gitignore_path = root_path / ".gitignore"
    
    if gitignore_path.exists():
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    clean_line = line.strip()
                    if clean_line and not clean_line.startswith("#"):
                        ignore_patterns.append(clean_line.rstrip('/'))
        except Exception:
            pass
    return ignore_patterns

def is_ignored(name: str, ignore_list: list) -> bool:
    """Checks if a file/folder matches any ignore pattern."""
    for pattern in ignore_list:
        if fnmatch.fnmatch(name, pattern) or name == pattern:
            return True
    return False

def get_color_for_file(filename: str) -> str:
    """Returns the appropriate ANSI color based on file extension."""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    if ext in ('py', 'pyc', 'pyw'): return C.YELLOW
    if ext in ('md', 'txt', 'csv', 'log'): return C.GREEN
    if ext in ('json', 'toml', 'yaml', 'yml', 'ini', 'cfg'): return C.MAGENTA
    if ext in ('sh', 'bat', 'exe', 'dll', 'so'): return C.RED
    return C.RESET

def format_size(size_in_bytes: int) -> str:
    """Formats bytes into human-readable strings."""
    size = float(size_in_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:3.1f}{unit}"
        size /= 1024.0
    return f"{size:.1f}TB"

def generate_tree_lines(dir_path: Path, ignore_list: list, prefix: str = "", show_all: bool = False, show_stats: bool = False) -> list:
    """Recursively builds the file structure and returns a list of strings."""
    lines = []
    try:
        contents = []
        for p in dir_path.iterdir():
            if not show_all and is_ignored(p.name, ignore_list):
                continue
            contents.append(p)
            
        contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        pointers = [("├── ", "│   "), ("└── ", "    ")]

        for i, path in enumerate(contents):
            is_last = (i == len(contents) - 1)
            pointer, indent = pointers[1] if is_last else pointers[0]

            if path.is_dir():
                lines.append(f"{prefix}{pointer}{C.BOLD}{C.CYAN}{path.name}/{C.RESET}")
                lines.extend(generate_tree_lines(path, ignore_list, prefix + indent, show_all, show_stats))
            else:
                color = get_color_for_file(path.name)
                stat_str = ""
                if show_stats:
                    try:
                        size = format_size(path.stat().st_size)
                        stat_str = f" {C.BOLD}[{size:>7}]{C.RESET}"
                    except Exception:
                        stat_str = " [error]"
                        
                lines.append(f"{prefix}{pointer}{color}{path.name}{C.RESET}{stat_str}")

    except PermissionError:
        lines.append(f"{prefix}└── {C.RED}[Permission Denied]{C.RESET}")
    except Exception as e:
        lines.append(f"{prefix}└── {C.RED}[Error: {str(e)}]{C.RESET}")
    
    return lines

def strip_ansi(text: str) -> str:
    """Removes ANSI color codes for clean text file output."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def main():
    parser = argparse.ArgumentParser(description="Generate and display a clean directory tree.")
    parser.add_argument("path", nargs="?", default=".", help="The folder path to scan (defaults to current directory)")
    parser.add_argument("-o", "--output", dest="output_file", help="Path to save the output text file (e.g., -o tree.txt)")
    parser.add_argument("--all", action="store_true", help="Include hidden/junk directories like node_modules and .git")
    parser.add_argument("--stats", action="store_true", help="Show file sizes next to files")
    parser.add_argument("--llm", action="store_true", help="Format the output specifically for pasting into LLM prompts")
    
    args = parser.parse_args()

    user_input = args.path.strip()
    if user_input.startswith('"') and user_input.endswith('"'):
        user_input = user_input[1:-1]

    target_dir = Path(user_input).resolve()

    if not args.llm:
        print_banner()

    if not target_dir.exists():
        print(f" {C.RED}[!]{C.RESET} Error: The path '{target_dir}' does not exist.")
        sys.exit(1)
    if not target_dir.is_dir():
        print(f" {C.RED}[!]{C.RESET} Error: The path '{target_dir}' is not a directory.")
        sys.exit(1)

    if not args.llm:
        print(f" {C.CYAN}[*]{C.RESET} Scanning: {C.YELLOW}{target_dir}{C.RESET}")

    ignore_list = parse_gitignore(target_dir)

    output_lines = []
    
    if args.llm:
        output_lines.append("Here is my project structure:")
        output_lines.append("```text")
        
    output_lines.append(f"Directory Tree for: {target_dir}")
    output_lines.append("=" * 50)
    output_lines.append(f"{C.BOLD}{C.CYAN}{target_dir.name or str(target_dir)}/{C.RESET}")
    
    tree_lines = generate_tree_lines(target_dir, ignore_list, show_all=args.all, show_stats=args.stats)
    
    if not tree_lines:
        print(f" {C.RED}[!]{C.RESET} Directory is empty or all contents were skipped.")
        sys.exit(0)
        
    output_lines.extend(tree_lines)
    
    if args.llm:
        output_lines.append("```")
        
    final_output_colored = "\n".join(output_lines)

    print("\n" + final_output_colored + "\n")

    if args.output_file:
        out_path = Path(args.output_file).resolve()
        try:
            clean_output = strip_ansi(final_output_colored)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(clean_output + "\n")
            if not args.llm:
                print(f" {C.GREEN}[✓]{C.RESET} Success! Tree saved to {C.YELLOW}{out_path}{C.RESET}")
        except Exception as e:
            print(f" {C.RED}[!]{C.RESET} Error saving to file: {e}")
    else:
        if not args.llm:
            print(f" {C.GREEN}[✓]{C.RESET} Scan complete.")

if __name__ == "__main__":
    main()
