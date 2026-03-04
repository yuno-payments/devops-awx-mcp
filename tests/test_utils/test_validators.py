import pytest

from src.utils.validators import validate_json, validate_scm_type, validate_verbosity


class TestValidateJson:
    def test_valid_json(self):
        result = validate_json('{"key": "value"}', "test_field")
        assert result == {"key": "value"}

    def test_valid_empty_json(self):
        result = validate_json("{}", "test_field")
        assert result == {}

    def test_valid_json_array(self):
        result = validate_json('[1, 2, 3]', "test_field")
        assert result == [1, 2, 3]

    def test_invalid_json(self):
        with pytest.raises(ValueError, match="Invalid JSON in test_field"):
            validate_json("not json", "test_field")

    def test_empty_string(self):
        with pytest.raises(ValueError, match="Invalid JSON in variables"):
            validate_json("", "variables")


class TestValidateScmType:
    def test_valid_types(self):
        for scm_type in ["", "git", "hg", "svn", "manual"]:
            validate_scm_type(scm_type)  # Should not raise

    def test_invalid_type(self):
        with pytest.raises(ValueError, match="Invalid SCM type"):
            validate_scm_type("mercurial")


class TestValidateVerbosity:
    def test_valid_levels(self):
        for level in range(5):
            validate_verbosity(level)  # Should not raise

    def test_negative(self):
        with pytest.raises(ValueError, match="Verbosity must be between 0 and 4"):
            validate_verbosity(-1)

    def test_too_high(self):
        with pytest.raises(ValueError, match="Verbosity must be between 0 and 4"):
            validate_verbosity(5)
