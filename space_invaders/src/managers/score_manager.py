"""
Score Manager
Manages score tracking and high scores for the Space Invaders game.
"""

class ScoreManager:
    """
    Manages game scoring and high scores.
    
    Attributes:
        current_score (int): Current game score
        high_score (int): Highest score achieved
    """
    
    def __init__(self):
        """Initialize the score manager."""
        self.current_score = 0
        self.high_score = 0
        
    def add_points(self, points: int) -> None:
        """Add points to the current score."""
        self.current_score += points
        
    def get_score(self) -> int:
        """Get the current score."""
        return self.current_score
        
    def get_high_score(self) -> int:
        """Get the high score."""
        return self.high_score
        
    def update_high_score(self) -> None:
        """Update high score if current score is higher."""
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            
    def reset_score(self) -> None:
        """Reset the current score to zero."""
        self.current_score = 0
        
    def reset_all(self) -> None:
        """Reset both current and high scores."""
        self.current_score = 0
        self.high_score = 0