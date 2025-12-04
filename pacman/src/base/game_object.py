"""
GameObject Base Class

Base class for all game entities.
"""

class GameObject:
    """Base class for all game objects."""

    def __init__(self, position=(0, 0), size=(1, 1)):
        """
        Initialize a game object.

        Args:
            position: Tuple (x, y) representing the object's position
            size: Tuple (width, height) representing the object's size
        """
        self.position = position
        self.size = size
        self.active = True

    def update(self, dt):
        """
        Update the game object.

        Args:
            dt: Delta time in seconds since last update
        """
        pass

    def render(self, surface):
        """
        Render the game object.

        Args:
            surface: Pygame surface to render on
        """
        pass

    def get_position(self):
        """Get the current position of the object."""
        return self.position

    def set_position(self, position):
        """Set the position of the object."""
        self.position = position

    def get_size(self):
        """Get the size of the object."""
        return self.size

    def set_size(self, size):
        """Set the size of the object."""
        self.size = size

    def is_active(self):
        """Check if the object is active."""
        return self.active

    def set_active(self, active):
        """Set the active state of the object."""
        self.active = active