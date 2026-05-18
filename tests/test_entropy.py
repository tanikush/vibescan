import pytest
from vibescan.rules.entropy import shannon_entropy, find_high_entropy_strings


class TestShannonEntropy:
    def test_empty_string_returns_zero(self):
        """Test that empty string returns 0 entropy"""
        assert shannon_entropy("", "abc") == 0.0
    
    def test_single_char_returns_zero(self):
        """Test that single character returns 0 entropy"""
        assert shannon_entropy("a", "abc") == 0.0
    
    def test_uniform_distribution_max_entropy(self):
        """Test that uniform character distribution gives high entropy"""
        result = shannon_entropy("abcd", "abcd")
        assert result > 1.0
    
    def test_low_entropy_repeated_chars(self):
        """Test that repeated characters give low entropy"""
        result = shannon_entropy("aaaaaaaa", "a")
        assert result == 0.0
    
    def test_mixed_charset(self):
        """Test entropy with mixed characters"""
        result = shannon_entropy("abc123", "abcdefghijklmnopqrstuvwxyz0123456789")
        assert result > 0


class TestFindHighEntropyStrings:
    def test_find_base64_entropy_strings(self):
        """Test finding high entropy base64 strings"""
        content = "random_string = 'QUJDREVGR0hJRTIzNDU2Nzg5MDEyMzQ1Njc4OQ=='"
        findings = find_high_entropy_strings(content, min_length=20, threshold=4.0)
        
        assert len(findings) >= 1
        assert any(4.0 < score for _, score in findings)
    
    def test_no_entropy_strings_below_threshold(self):
        """Test that normal text doesn't trigger entropy detection"""
        content = "this is just normal text without any secrets"
        findings = find_high_entropy_strings(content, min_length=20, threshold=4.0)
        
        assert len(findings) == 0
    
    def test_hex_strings_detected(self):
        """Test that hex strings are detected"""
        content = "token = 'a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef'"
        findings = find_high_entropy_strings(content, min_length=40, threshold=3.5)
        
        assert len(findings) >= 1
    
    def test_min_length_respected(self):
        """Test that min_length parameter is respected"""
        content = "short = 'abc123'"
        findings = find_high_entropy_strings(content, min_length=100, threshold=4.0)
        
        assert len(findings) == 0
    
    def test_threshold_respected(self):
        """Test that threshold parameter filters results"""
        content = "random_text_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        findings_low = find_high_entropy_strings(content, min_length=20, threshold=2.0)
        findings_high = find_high_entropy_strings(content, min_length=20, threshold=5.0)
        
        assert len(findings_low) >= len(findings_high)


class TestEntropyIntegration:
    def test_real_world_secret_detection(self):
        """Test detection of realistic secret-like strings"""
        content = '''
        api_key = "sk-abcdefghijklmnopqrstuvwxyz12345678901234567890"
        token = "ghp_abcdefghijklmnopqrstuvwxyz12345678901234567890"
        '''
        findings = find_high_entropy_strings(content, min_length=30, threshold=4.0)
        
        assert len(findings) >= 1