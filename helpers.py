def string_contains_text(string, substring):
    try:
        assert substring in string, f"'{substring}' not found in '{string}'"
        return True
    except AssertionError:
        return False