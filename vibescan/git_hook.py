import os
import stat
from pathlib import Path
import click
from rich.console import Console

console = Console()

PRE_PUSH_CONTENT = '''#!/bin/sh
echo "[ VibeScan ] Scanning..."
vibescan scan . --fail-on-critical
if [ $? -ne 0 ]; then
    echo  "PUSH BLOCKED — Fix security issues first!"
    exit 1
fi
exit 0
'''

def install_hooks():
    git_dir = Path('.git')
    if not git_dir.exists():
        console.print('[red]Error: Git repository not found. Run git init first.[/]')
        return False
    
    hook_path = git_dir / 'hooks' / 'pre-push'
    hook_path.write_text(PRE_PUSH_CONTENT)
    
    # Make executable
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IEXEC)
    
    console.print('[green]OK Git hooks installed successfully![/]')
    console.print('[cyan]  pre-push hook will now scan before every push.[/]')
    return True
