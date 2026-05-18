import os
import re
from pathlib import Path
from typing import List, Dict, Any
from .rules.secrets import SECRET_PATTERNS
from .rules.vibe_patterns import VIBE_PATTERNS
from .rules.entropy import find_high_entropy_strings
from .rules.ai_risk_patterns import AI_RISK_PATTERNS
from .config import VibeScanConfig

SKIP_EXTENSIONS = {'.jpg', '.png', '.gif', '.svg', '.ico', '.pdf', '.zip', '.tar', '.gz', '.lock', '.pyc', '.pyo'}
SKIP_DIRS = {'node_modules', '.git', 'venv', '__pycache__', 'dist', 'build', '.next', '.eggs', 'vibescan.egg-info'}

class Finding:
    '''Represents a single security finding'''
    def __init__(self, file_path, line_no, pattern_name, matched_text, risk_level, description=''):
        self.file_path = file_path
        self.line_no = line_no
        self.pattern_name = pattern_name
        self.matched_text = matched_text[:60] + '...' if len(matched_text) > 60 else matched_text
        self.risk_level = risk_level
        self.description = description
    
    def to_dict(self) -> Dict:
        return {
            'file': str(self.file_path),
            'line': self.line_no,
            'pattern': self.pattern_name,
            'match': self.matched_text,
            'risk': self.risk_level,
            'description': self.description
        }

class VibeScan:
    def __init__(self, path: str, include_vibe: bool = True):
        self.path = Path(path)
        self.include_vibe = include_vibe
        self.findings: List[Finding] = []
        self.files_scanned = 0
        self.config = VibeScanConfig()
    
    def scan(self) -> List[Finding]:
        '''Entry point - scan folder or file for security issues'''
        if self.path.is_file():
            self._scan_file(self.path)
        else:
            self._scan_directory(self.path)
        return self.findings
    
    def _scan_directory(self, directory: Path):
        for root, dirs, files in os.walk(directory):
            # Skip unnecessary directories
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix not in SKIP_EXTENSIONS:
                    self._scan_file(filepath)
    
    def _is_filtered(self, filepath: Path) -> bool:
        """Check if file should be filtered based on config"""
        str_path = str(filepath)
        if self.config.should_skip_path(str_path):
            return True
        return False
    
    def _scan_file(self, filepath: Path):
        if self._is_filtered(filepath):
            return
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            self.files_scanned += 1
            
            self._apply_patterns(filepath, content, SECRET_PATTERNS)
            if self.include_vibe:
                self._apply_patterns(filepath, content, VIBE_PATTERNS)
            self._apply_entropy(filepath, content)
            self._apply_patterns(filepath, content, AI_RISK_PATTERNS)
        except (PermissionError, OSError):
            pass
    
    def _apply_patterns(self, filepath, content, patterns):
        lines = content.split('\n')
        for pattern_data in patterns:
            pattern_name, regex, risk = pattern_data[:3]
            description = pattern_data[3] if len(pattern_data) > 3 else ''
            
            # Skip excluded patterns
            if self.config.should_skip_pattern(pattern_name):
                continue
            
            for line_no, line in enumerate(lines, 1):
                            match = re.search(regex, line)
                            if match:
                                matched_text = match.group()
                                # Skip allowlisted
                                if self.config.is_allowlisted(matched_text):
                                    continue
                                self.findings.append(Finding(
                                    filepath, line_no, pattern_name,
                                        matched_text, risk, description
                            ))
    
    def _apply_entropy(self, filepath, content):
        for secret, score in find_high_entropy_strings(content):
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if secret in line:
                    self.findings.append(Finding(
                        filepath, i,
                        f'High Entropy String (score={score:.2f})',
                        secret, 'HIGH',
                        'Possible secret detected by entropy analysis'
                    ))
                    break
    
    @property
    def risk_summary(self) -> Dict[str, int]:
        return {
            'CRITICAL': sum(1 for f in self.findings if f.risk_level == 'CRITICAL'),
            'HIGH': sum(1 for f in self.findings if f.risk_level == 'HIGH'),
            'MEDIUM': sum(1 for f in self.findings if f.risk_level == 'MEDIUM'),
        }
