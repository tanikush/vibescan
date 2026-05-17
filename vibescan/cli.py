import click
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from .scanner import VibeScan
from .reporter import generate_html_report
from .team_report import generate_dashboard

console = Console()

@click.group()
def cli():
    '''VibeScan — AI-Generated Code Security Scanner'''
    pass

@cli.command()
@click.argument('path', default='.')
@click.option('--output', '-o', default=None, help='Save HTML report: -o report.html')
@click.option('--dashboard', '-d',
              default=None,
              help='Generate dashboard HTML')
@click.option('--json-out', '-j', default=None, help='Save JSON output: -j results.json')
@click.option('--no-vibe', is_flag=True, help='Skip vibe patterns, scan secrets only')
@click.option('--fail-on-critical', is_flag=True, help='Exit with code 1 if CRITICAL issues found (for CI/CD)')
def scan(path, output, dashboard, json_out, no_vibe, fail_on_critical):
    '''Scan folder or file for security issues'''
    
    console.print(Panel(
        '[bold green]VibeScan[/] — AI Code Security Scanner\n'
        f'Scanning: [cyan]{path}[/]',
        border_style='green'
    ))
    
    scanner = VibeScan(path, include_vibe=not no_vibe)
    with console.status('[green]Scanning files...[/]'):
        findings = scanner.scan()
    
    summary = scanner.risk_summary
    
    if findings:
        table = Table(title='Security Findings', box=box.ROUNDED)
        table.add_column('File', style='cyan', no_wrap=False)
        table.add_column('Line', style='yellow', width=6)
        table.add_column('Issue', style='white')
        table.add_column('Risk', style='bold', width=10)
        table.add_column('Match', style='red', no_wrap=False)
        
        risk_colors = {
            'CRITICAL': '[bold red]CRITICAL[/]',
            'HIGH': '[bold yellow]HIGH[/]',
            'MEDIUM': '[yellow]MEDIUM[/]',
        }
        
        for f in findings:
            table.add_row(
                str(f.file_path),
                str(f.line_no),
                f.pattern_name,
                risk_colors.get(f.risk_level, f.risk_level),
                f.matched_text
            )
        
        console.print(table)
    else:
        console.print('[bold green]OK - No issues found! Code is clean.[/]')
    
    console.print(f'\nFiles scanned: [cyan]{scanner.files_scanned}[/]')
    console.print(f'Critical: [red]{summary["CRITICAL"]}[/]  '
                  f'High: [yellow]{summary["HIGH"]}[/]  '
                  f'Medium: [yellow]{summary["MEDIUM"]}[/]')
    
    if output:
        generate_html_report(findings, scanner, output)
        console.print(f'\n[green]OK Report saved:[/] {output}')

    if dashboard:
        generate_dashboard(findings, scanner, dashboard)
        console.print(
            f'[green]OK Dashboard saved:[/] {dashboard}'
    )
    
    if json_out:
        with open(json_out, 'w') as f:
            json.dump([x.to_dict() for x in findings], f, indent=2)
        console.print(f'[green]OK JSON saved:[/] {json_out}')
    
    if fail_on_critical and summary['CRITICAL'] > 0:
        sys.exit(1)

def main():
    cli()

if __name__ == '__main__':
    main()
