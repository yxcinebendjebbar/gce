import argparse
import subprocess
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from rich.text import Text

console = Console()


def get_git_changes():
    """Fetches staged changes from Git and counts file/line modifications."""
    try:
        files_result = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            capture_output=True, text=True, check=True, encoding="utf-8"
        )
        changed_files = files_result.stdout.strip().split("\n")

        diff_result = subprocess.run(
            ["git", "diff", "--staged", "--numstat"], 
            capture_output=True, text=True, check=True, encoding="utf-8"
        )
        diff_lines = diff_result.stdout.strip().split("\n")

       
        total_added = 0
        total_removed = 0
        for line in diff_lines:
            parts = line.split("\t")
            if len(parts) == 3:  
                added, removed, _ = parts
                total_added += int(added) if added.isdigit() else 0
                total_removed += int(removed) if removed.isdigit() else 0

        
        diff_text = diff_result.stdout.strip()
        return changed_files if changed_files != [""] else [], total_added, total_removed, diff_text

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Error fetching Git changes:[/bold red] {e}")
        return [], 0, 0, ""



def extract_relevant_changes(diff_text):
    """Extracts meaningful code changes from Git diff output."""
    changes = []
    for line in diff_text.split("\n"):
       
        if line.startswith("+") and not line.startswith("+++"):
            changes.append(line[1:].strip())  # Remove '+' sign
    return changes

def classify_changes(changes):
    """Classifies extracted code changes into categories."""
    categories = {"[green]Added[/green]": [], "[yellow]Updated[/yellow]": [], "[red]Fixed[/red]": []}

    for change in changes:
        if any(word in change.lower() for word in ["add", "create", "new", "insert"]):
            categories["[green]Added[/green]"].append(change)
        elif any(word in change.lower() for word in ["update", "modify", "change", "refactor"]):
            categories["[yellow]Updated[/yellow]"].append(change)
        elif any(word in change.lower() for word in ["fix", "resolve", "correct", "bug"]):
            categories["[red]Fixed[/red]"].append(change)
        else:
            categories["[yellow]Updated[/yellow]"].append(change) 

    return categories

def generate_commit_message(categories):
    """Generates a structured commit message."""
    commit_parts = []
    for category, changes in categories.items():
        if changes:
            commit_parts.append(f"{category}: {changes[0]}")  
    return " | ".join(commit_parts) if commit_parts else "Updated codebase"

def display_summary(files, total_added, total_removed, commit_message):
    """Displays a sleek commit summary with stats."""
    console.print("\n[bold cyan]📂 Changed Files:[/bold cyan]")
    for file in files:
        console.print(f" - [bold white]{file}[/bold white]")

    console.print("\n[bold cyan]📊 Commit Stats:[/bold cyan]")
    console.print(f"📄 Files Changed: [bold yellow]{len(files)}[/bold yellow]")
    console.print(f"➕ Lines Added: [bold green]{total_added}[/bold green]")
    console.print(f"➖ Lines Removed: [bold red]{total_removed}[/bold red]")

    console.print("\n[bold cyan]✍ Suggested Commit Message:[/bold cyan]")
    console.print(f"[bold green]{commit_message}[/bold green]")



def assign_emoji(commit_message):
    """Adds appropriate emojis based on commit content."""
    emoji_map = {
        "add": "✨", "create": "✨", "new": "✨",  # Features
        "fix": "🐛", "bug": "🐛", "resolve": "🐛",  # Bug fixes
        "refactor": "🧹", "cleanup": "🧹", "optimize": "🧹"  # Refactoring
    }

    for keyword, emoji in emoji_map.items():
        if keyword in commit_message.lower():
            return f"{emoji} {commit_message}"

    return f"📌 {commit_message}"  

def format_commit_message(commit_message, use_gitmoji=True):
    """Formats the commit message based on the chosen style."""
    gitmoji_map = {
        "✨": ":sparkles:",
        "🐛": ":bug:",
        "🧹": ":broom:",
        "📌": ":pushpin:"
    }

    if use_gitmoji:
        for emoji, gitmoji in gitmoji_map.items():
            commit_message = commit_message.replace(emoji, gitmoji)

    return commit_message


def main():
    parser = argparse.ArgumentParser(description="✨ Enhanced Git Commit CLI ✨")
    parser.add_argument("message", type=str, nargs="?", default="", help="Commit message (optional)")
    parser.add_argument("--gitmoji", action="store_true", help="Use Gitmoji format instead of emojis")
    args = parser.parse_args()

    changed_files, total_added, total_removed, diff_text = get_git_changes()
    if not changed_files:
        console.print("[bold yellow]⚠ No staged changes found. Please stage your files using 'git add'.[/bold yellow]")
        return

    extracted_changes = extract_relevant_changes(diff_text)
    categorized_changes = classify_changes(extracted_changes)
    suggested_commit = generate_commit_message(categorized_changes)
    decorated_commit = assign_emoji(suggested_commit)
    final_commit = format_commit_message(decorated_commit, args.gitmoji)

    display_summary(changed_files, total_added, total_removed, final_commit)

    if Confirm.ask("\n✅ Accept this commit message?"):
        subprocess.run(["git", "commit", "-m", final_commit])
        console.print("[bold green]✔ Commit successful![/bold green]")
    else:
        console.print("[bold red]❌ Commit aborted.[/bold red]")
if __name__ == "__main__":
    main()
