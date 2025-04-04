import subprocess
import argparse
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from rich.text import Text

console = Console()


def get_git_diff():

    """Fetches the staged git diff."""
    try:
        result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print("Error fetching git diff:", e)
        return None


def get_git_changes():
    try:
        # Get changed file names
        files_result = subprocess.run(
            ["git", "diff", "--staged", "--name-only"],
            capture_output=True, text=True, check=True
        )
        changed_files = files_result.stdout.strip().split("\n")

        # Get actual code changes
        diff_result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True, text=True, check=True
        )
        changes = diff_result.stdout.strip()

        return changed_files if changed_files != [""] else [], changes

    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error fetching Git changes:[/bold red] {e}")
        return [], ""


def extract_relevant_changes(diff_text):
    """Extract meaningful code changes from Git diff output."""
    changes = []
    for line in diff_text.split("\n"):
        # Ignore metadata lines, only keep actual code changes
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
            categories["[yellow]Updated[/yellow]"].append(change)  # Default to "Updated"


    return categories


def generate_commit_message(categories):
    """Generate a commit message based on classified changes."""
    commit_parts = []

    for category, changes in categories.items():
        if changes:
            commit_parts.append(f"{category}: {changes[0]}")  # Use first detected change
    
    return " | ".join(commit_parts) if commit_parts else "Updated codebase"


def display_summary(files, categories, commit_message):
    """Displays a sleek summary using Rich tables and styling."""
    console.print("\n[bold cyan]📂 Changed Files:[/bold cyan]")
    for file in files:
        console.print(f" - [bold white]{file}[/bold white]")

    console.print("\n[bold cyan]🔍 Extracted Changes:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category", style="bold", justify="left")
    table.add_column("Example Change", style="white", justify="left")

    for category, changes in categories.items():
        if changes:
            table.add_row(category, changes[0])

    console.print(table)
    
    console.print("\n[bold cyan]✍ Suggested Commit Message:[/bold cyan]")
    console.print(f"[bold green]{commit_message}[/bold green]")




def main():
    parser = argparse.ArgumentParser(description="✨ Enhanced Git Commit CLI ✨")
    parser.add_argument("message", type=str, nargs="?", default="", help="Commit message (optional)")
    args = parser.parse_args()

    changed_files, diff_text = get_git_changes()
    if not changed_files:
        console.print("[bold yellow]⚠ No staged changes found. Please stage your files using 'git add'.[/bold yellow]")
        return

    extracted_changes = extract_relevant_changes(diff_text)
    categorized_changes = classify_changes(extracted_changes)
    suggested_commit = generate_commit_message(categorized_changes)

    display_summary(changed_files, categorized_changes, suggested_commit)

    if Confirm.ask("\n✅ Accept this commit message?"):
        subprocess.run(["git", "commit", "-m", suggested_commit])
        console.print("[bold green]✔ Commit successful![/bold green]")
    else:
        console.print("[bold red]❌ Commit aborted.[/bold red]")


if __name__ == "__main__":
    main()
