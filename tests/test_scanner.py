import pytest
from vibescan.scanner import VibeScan, Finding
from vibescan.rules.secrets import SECRET_PATTERNS


class TestVibeScan:
    def test_scan_file_with_secrets(self, tmp_path):
        """Test scanning a file with hardcoded secrets"""
        test_file = tmp_path / "test.py"
        test_file.write_text("api_key = 'AKIAIOSFODNN7EXAMPLE'\n")
        
        scanner = VibeScan(str(test_file))
        findings = scanner.scan()
        
        assert len(findings) >= 1
        assert any('AWS Access Key' in f.pattern_name for f in findings)
    
    def test_scan_directory(self, tmp_path):
        """Test scanning a directory with multiple files"""
        (tmp_path / "file1.py").write_text("password = 'mypassword123'\n")
        (tmp_path / "file2.py").write_text("normal code\n")
        
        scanner = VibeScan(str(tmp_path))
        findings = scanner.scan()
        
        assert scanner.files_scanned == 2
        assert len(findings) >= 1
    
    def test_skip_binary_files(self, tmp_path):
        """Test that binary files are skipped"""
        test_file = tmp_path / "image.png"
        test_file.write_bytes(b'\x89PNG\r\n\x1a\n')
        
        scanner = VibeScan(str(test_file))
        findings = scanner.scan()
        
        assert scanner.files_scanned == 1
        assert len(findings) == 0
    
    def test_risk_summary(self, tmp_path):
        """Test risk summary calculation"""
        test_file = tmp_path / "test.py"
        test_file.write_text("api_key = 'AKIAIOSFODNN7EXAMPLE'\nDEBUG = True\n")
        
        scanner = VibeScan(str(test_file))
        scanner.scan()
        summary = scanner.risk_summary
        
        assert 'CRITICAL' in summary
        assert 'HIGH' in summary
        assert 'MEDIUM' in summary
        assert summary['CRITICAL'] >= 1
    
    def test_finding_to_dict(self):
        """Test Finding serialization"""
        finding = Finding(
            file_path="test.py",
            line_no=10,
            pattern_name="Test Pattern",
            matched_text="test_value",
            risk_level="HIGH",
            description="Test description"
        )
        
        d = finding.to_dict()
        assert d['file'] == "test.py"
        assert d['line'] == 10
        assert d['pattern'] == "Test Pattern"
        assert d['risk'] == "HIGH"


class TestSecretsPatterns:
    def test_aws_key_pattern(self):
        """Test AWS key pattern exists"""
        assert any('AWS Access Key' in p[0] for p in SECRET_PATTERNS)
    
    def test_openai_pattern(self):
        """Test OpenAI key pattern exists"""
        assert any('OpenAI' in p[0] for p in SECRET_PATTERNS)
    
    def test_github_token_pattern(self):
        """Test GitHub token pattern exists"""
        assert any('GitHub Token' in p[0] for p in SECRET_PATTERNS)