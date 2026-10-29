"""Basic test for turtle_controller package."""


def test_import():
    """Test that the package can be imported."""
    try:
        import solution.turtle_controller as turtle_controller

        assert True
    except ImportError:
        assert False, "Failed to import turtle_controller package"
