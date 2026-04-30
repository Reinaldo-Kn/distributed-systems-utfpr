# Distributed Systems - UTFPR

This repository contains projects developed for the Distributed Systems course at UTFPR.

## Repository Structure

Each folder in this repository represents a project from the course.

Inside each project folder, you will find its own `README.md` file with:
- an explanation of the proposed solution;
- instructions on how to run the code.

## Python Package Management

All projects use `uv` to manage Python packages and environments.

## Installing Dependencies with uv

From a project folder (the one containing `pyproject.toml`), install all dependencies:

```bash
uv sync
```

To add a new dependency to a project:

```bash
uv add package-name
```

To run Python commands inside the project environment:

```bash
uv run python your_script.py
```

For Project 2, you can run automatic with the bash script, but `tmux` is required:

```bash
./project-2-rmi-cat-babysitter/run_all.sh
```
Tmux uses similar commands as vim, to enter the command mode, press `Ctrl + b` and then the desired command. For example, to get out of a tmux session, you can press `Ctrl + b` and then `d` to detach from the session. 
To end all tmux sessions:
```bash
tmux kill-server
```
