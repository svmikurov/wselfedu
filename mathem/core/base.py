class Task:
    """Simple base class for all tasks."""

    def __init__(self, **kwargs):
        """Constructor."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_attr(self, attr):
        """Get class attribute."""
        return


class Addition:
    """Class of mathematical tasks on addition."""
