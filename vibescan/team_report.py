from pathlib import Path

def calculate_score(findings):
    score = 100

    for f in findings:
        if f.risk_level == 'CRITICAL':
            score -= 20
        elif f.risk_level == 'HIGH':
            score -= 10
        elif f.risk_level == 'MEDIUM':
            score -= 3

    return max(0, score)


def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 75:
        return 'B'
    elif score >= 60:
        return 'C'
    elif score >= 40:
        return 'D'
    return 'F'


def generate_dashboard(findings, scanner, output='dashboard.html'):
    score = calculate_score(findings)
    grade = get_grade(score)

    rows = ""

    for f in findings:
        rows += f"""
        <tr>
            <td>{f.file_path}</td>
            <td>{f.line_no}</td>
            <td>{f.pattern_name}</td>
            <td>{f.risk_level}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>VibeScan Dashboard</title>
        <style>
        body {{
            font-family: Arial;
            padding:20px;
        }}

        table {{
            width:100%;
            border-collapse: collapse;
        }}

        td,th {{
            border:1px solid black;
            padding:8px;
        }}
        </style>
    </head>

    <body>

    <h2>Security Score: {score}/100</h2>
    <h2>Grade: {grade}</h2>

    <h1>VibeScan Dashboard</h1>

    <p>Files scanned: {scanner.files_scanned}</p>

    <p>Critical: {scanner.risk_summary['CRITICAL']}</p>
    <p>High: {scanner.risk_summary['HIGH']}</p>
    <p>Medium: {scanner.risk_summary['MEDIUM']}</p>

    <h2>Findings</h2>

    <table>
        <tr>
            <th>File</th>
            <th>Line</th>
            <th>Issue</th>
            <th>Risk</th>
        </tr>

        {rows}

    </table>

    </body>
    </html>
    """

    Path(output).write_text(
        html,
        encoding='utf-8'
    )