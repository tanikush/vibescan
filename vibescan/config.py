import yaml
import json
import fnmatch
from pathlib import Path
from typing import Set


DEFAULT = {
    'exclude_paths': ['tests/', 'docs/', 'node_modules/', '.git/'],
    'exclude_patterns': [],
    'allowlist': [],
    'entropy_threshold': 4.5,
    'baseline_file': None,
    'report_levels': ['CRITICAL', 'HIGH', 'MEDIUM'],
}


class VibeScanConfig:
    def __init__(self, config_path='.vibescan.yml'):
        self.cfg = DEFAULT.copy()
        p = Path(config_path)
        if p.exists():
            user = yaml.safe_load(p.read_text()) or {}
            self.cfg.update(user)
        self.baseline: Set[str] = set()
        bf = self.cfg.get('baseline_file')
        if bf and Path(bf).exists():
            self.baseline = set(json.loads(Path(bf).read_text()))

    def should_skip_path(self, filepath: str) -> bool:
        return any(fnmatch.fnmatch(filepath, f'*{p}*')
                   for p in self.cfg['exclude_paths'])

    def should_skip_pattern(self, name: str) -> bool:
        return name in self.cfg['exclude_patterns']

    def is_allowlisted(self, text: str) -> bool:
        return any(a in text for a in self.cfg['allowlist'])

    def is_in_baseline(self, fingerprint: str) -> bool:
        return fingerprint in self.baseline

    def save_baseline(self, findings, out='.vibescan_baseline.json'):
        fps = [f'{f.file_path}:{f.line_no}:{f.pattern_name}' for f in findings]
        Path(out).write_text(json.dumps(fps, indent=2))