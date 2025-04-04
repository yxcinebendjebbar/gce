from setuptools import setup, find_packages

setup(
    name="gce",
    version="1.0.0",
    packages=find_packages(), 
    install_requires=[
        "gitpython",  
        "inquirer",
        "rich",
    ],
    entry_points={
        'console_scripts': [
            'gce = main:main',  # The entry point to your CLI tool
        ],
    },
    # Add other metadata (author, description, etc.)
    author="yxcinebendjebbar",
    author_email="yacine.bbusiness@gmail.com",
    description="A CLI tool to enhance git commit messages with stats and emojis.",
    url="https://github.com/yourusername/git-commit-enhancer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
