"""
Game Manager
Coordinates all game systems and manages state transitions.
"""

import pygame
from typing import Dict, Optional, Type
from src.game.game_state import GameState
from src.game.states.start_state import StartState
from src.game.states.play_state import PlayState
from src.game.states.pause_state import PauseState
from src.game.states.game_over_state import GameOverState
from src.game.states.victory_state import VictoryState

class GameManager:
    """
    Main game manager that coordinates all systems.
    
    Responsibilities:
    - State management and transitions
    - Main game loop coordination
    - System integration
    """
    
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        """
        Initialize the game manager.
        
        Args:
            screen: The main display surface
            clock: The pygame clock for timing
        """
        self.screen = screen
        self.clock = clock
        self.running = True
        
        # Initialize state classes
        self.states: Dict[str, GameState] = {
            'start': StartState(),
            'play': PlayState(),
            'pause': PauseState(),
            'game_over': GameOverState(),
            'victory': VictoryState()
        }
        
        # Set initial state
        self.current_state = self.states['start']
        self.current_state.on_enter(self)
    
    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events.
        
        Args:
            event: The pygame event to handle
        """
        new_state = self.current_state.handle_events(event)
        
        if new_state and new_state in self.states:
            self.change_state(new_state)
    
    def update(self, dt: float) -> None:
        """
        Update the current game state.
        
        Args:
            dt: Delta time in seconds
        """
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self) -> None:
        """Render the current game state."""
        if self.current_state:
            self.current_state.render(self.screen)
    
    def change_state(self, state_name: str) -> None:
        """
        Change to a new game state.
        
        Args:
            state_name: The name of the state to change to
        """
        if state_name in self.states:
            # Exit current state
            if self.current_state:
                self.current_state.on_exit()
            
            # Enter new state
            self.current_state = self.states[state_name]
            self.current_state.on_enter(self)
    
    def get_state(self, state_name: str) -> Optional[GameState]:
        """
        Get a specific state.
        
        Args:
            state_name: The name of the state
            
        Returns:
            The requested state or None
        """
        return self.states.get(state_name)
    
    def is_running(self) -> bool:
        """Check if the game is still running."""
        return self.running
    
    def stop(self) -> None:
        """Stop the game."""
        self.running = False