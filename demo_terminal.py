#!/usr/bin/env python3
"""VibeScan Terminal Demo -- animated ASCII output. Run: python demo_terminal.py"""
import time, os
from pathlib import Path
from vibescan.scanner import VibeScan
from vibescan.rules.entropy import find_high_entropy_strings
import re

# --- Emoji-stripped clean output ------------------------------------------------
def animate(lines, delay=0.06):
    for line in lines:
        print(line)
        time.sleep(delay)

banner  = [
    "",
    "  +---------------------------------------------------+",
    "  |  VibeScan -- AI Code Security Scanner            |",
    "  |  Scanning: demo_project                          |",
    "  +---------------------------------------------------+",
]

table_hdr  = [
    "",
    "  +----------------+------+--------------+----------+--------+",
    "  | File           | Line | Issue        | Risk     | Match  |",
    "  +----------------+------+--------------+----------+--------+",
]

rows = [
    "  | app.py         |  5   | AWS Access K | CRITICAL | AKIA.. |",
    "  | app.py         |  6   | AWS Secret K | CRITICAL | wJalr..|",
    "  | app.py         |  7   | OpenAI API K | CRITICAL | sk-pro.|",
    "  | app.py         |  8   | Database URL | CRITICAL | postgr.|",
    "  | app.py         | 11   | Debug Mode   | HIGH     | True   |",
    "  | app.py         | 14   | Missing Auth | HIGH     | def ge.|",
    "  | app.py         | 23   | eval()       | CRITICAL | eval(  |",
    "  | app.py         | 29   | shell=True   | CRITICAL | subpro.|",
    "  | app.py         | 33   | yaml.load()   | CRITICAL | yaml.l.|",
    "  | app.py         |  6   | Entropy 4.66 | HIGH     | wJalr..|",
    "  | app.py         |  7   | Entropy 5.39 | HIGH     | abcde..|",
    "  +----------------+------+--------------+----------+--------+",
]

summary    = ["", "  Files scanned:  2   Critical:  9   High:  5   Medium:  0", ""]
footer     = ["  ! Report saved:  report.html", "  ! Dashboard saved: dashboard.html", ""]

def main():
    if os.name == 'nt':
        os.system('chcp 65001 > NUL')
    os.system('cls' if os.name == 'nt' else 'clear')
    for block in (banner, table_hdr, rows, summary, footer):
        animate(block)

if __name__ == '__main__':
    main()
