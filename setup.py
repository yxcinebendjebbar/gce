from setuptools import setup, find_packages

setup(
    name="gce",
    version="1.0.1",
    packages=find_packages(), 
    install_requires=[
        "gitpython",  
        "inquirer",
        "rich",
    ],
    entry_points={
        'console_scripts': [
            'gce = gce.main:main',
        ],
    },
    author="yxcinebendjebbar",
    author_email="yacine.bbusiness@gmail.com",
    description="A CLI tool to enhance git commit messages with stats and emojis.",
    url="https://github.com/yxcinebendjebbar/gce",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
