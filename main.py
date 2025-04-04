import subprocess
import argparse

def get_git_diff():
    """Fetches the staged git diff."""
    try:
        result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print("Error fetching git diff:", e)
        return None

def main():
    parser = argparse.ArgumentParser(description="Git Commit Enhancer")
    parser.add_argument("message", type=str, help="Commit message hint (optional)")
    args = parser.parse_args()
    
    diff = get_git_diff()
    if not diff:
        print("No staged changes detected.")
        return
    
    print("Git Diff:")
    print(diff)
    
    # Placeholder for AI-based commit message generation
    print("\nSuggested Commit Message:")
    print(f"feat: {args.message}")
    
    # Commit the changes (commented out for safety)
    # subprocess.run(["git", "commit", "-m", f"feat: {args.message}"])
    
if __name__ == "__main__":
    main()
