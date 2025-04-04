# GCE | Git Commit Enhancer

GCE (Git Commit Enhancer) is a CLI tool that enhances your Git commit messages by adding stats, emojis, and auto-decorations to keep them clear, concise, and easy to understand. It supports integration with both **Gitmoji** and **Conventional Commits** formats.

## Features

- **Commit Stats**: Adds file and line counts for each commit.
- **Auto Emojis**: Automatically adds emojis like ✨ for features, 🐛 for bug fixes, and 🧹 for refactors.
- **Gitmoji Support**: Choose to format your commits using Gitmoji.
- **Conventional Commits**: Auto-generate commits following the Conventional Commits specification.
- **Customizable**: Adjust settings for personal or team preferences.

## Installation

To install **GCE** locally:

1. Clone the repository:

   ```bash
   > git clone https://github.com/yourusername/git-commit-enhancer.git
   > cd git-commit-enhancer
   ```

2. Install the tool using pip:

```bash

> pip install .
```

## Usage

Once installed, you can use GCE directly from your command line:

```bash
> gce
```

Example:

```bash
> ~ git:(main) git add .
> ~ git:(main)  gce

📂 Changed Files:
 - .gitignore

📊 Commit Stats:
📄 Files Changed: 1
➕ Lines Added: 3
➖ Lines Removed: 0

✍ Suggested Commit Message:
📌 Updated codebase

✅ Accept this commit message? [y/n]: y
[main bab13f8] 📌 Updated codebase
 1 file changed, 3 insertions(+)
 create mode 100644 .gitignore
✔ Commit successful!

```

## Customization

You can customize the tool by modifying settings in the configuration file. Specify which format you'd like (Gitmoji or Conventional Commit) and whether you'd like to include file and line count stats.

## Contributing

We welcome contributions to GCE! If you'd like to help improve the project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
