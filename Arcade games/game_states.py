"""
Game state management system for the Arcade Collection.
Handles transitions between menu and different games, and provides a clean interface for state management.
"""

import pygame
from constants import GameState, SCREEN_WIDTH, SCREEN_HEIGHT


class GameStateManager:
    """
    Manages the current game state and handles state transitions.
    This class acts as the central controller for switching between different parts of the application.
    """
    
    def __init__(self, screen, clock):
        """
        Initialize the game state manager.
        
        Args:
            screen: Pygame surface for rendering
            clock: Pygame clock for timing
        """
        self.screen = screen
        self.clock = clock
        self.current_state = GameState.MENU
        self.state_handlers = {}
        self.state_data = {}
        
        # Initialize state handlers (will be set by the main game)
        self.menu_handler = None
        self.doom_game_handler = None
        self.contra_game_handler = None
        self.tetris_game_handler = None
        
        # Register state handlers
        self._register_state_handlers()
        
        print(f"GameStateManager initialized with state: {self.current_state}")
    
    def _register_state_handlers(self):
        """Register state handlers for each possible game state."""
        self.state_handlers = {
            GameState.MENU: self._handle_menu_state,
            GameState.DOOM_GAME: self._handle_doom_game_state,
            GameState.CONTRA_GAME: self._handle_contra_game_state,
            GameState.TETRIS_GAME: self._handle_tetris_game_state,
            GameState.QUIT: self._handle_quit_state
        }
    
    def set_state_handlers(self, menu_handler, doom_handler=None, contra_handler=None, tetris_handler=None):
        """
        Set the handlers for each game state.
        
        Args:
            menu_handler: Handler for the main menu
            doom_handler: Handler for the Doom game (placeholder)
            contra_handler: Handler for the Contra game (placeholder)
            tetris_handler: Handler for the Tetris game (placeholder)
        """
        self.menu_handler = menu_handler
        self.doom_game_handler = doom_handler
        self.contra_game_handler = contra_handler
        self.tetris_game_handler = tetris_handler
        
        print("State handlers registered successfully")
    
    def change_state(self, new_state, data=None):
        """
        Change to a new game state.
        
        Args:
            new_state: The new game state to transition to
            data: Optional data to pass to the new state
        """
        if new_state not in self.state_handlers:
            print(f"Warning: Unknown state {new_state}")
            return
        
        print(f"Changing state from {self.current_state} to {new_state}")
        self.current_state = new_state
        self.state_data = data or {}
        
        # Handle state-specific initialization
        self._handle_state_transition(new_state)
    
    def _handle_state_transition(self, state):
        """Handle any initialization or cleanup needed for state transitions."""
        if state == GameState.MENU:
            print("Transitioned to MENU state")
        elif state == GameState.DOOM_GAME:
            print("Transitioned to DOOM_GAME state")
        elif state == GameState.CONTRA_GAME:
            print("Transitioned to CONTRA_GAME state")
        elif state == GameState.TETRIS_GAME:
            print("Transitioned to TETRIS_GAME state")
        elif state == GameState.QUIT:
            print("Transitioned to QUIT state")
    
    def handle_events(self, events):
        """
        Handle Pygame events based on current state.
        
        Args:
            events: List of Pygame events
            
        Returns:
            bool: True if the game should continue, False if it should quit
        """
        handler = self.state_handlers.get(self.current_state)
        if handler:
            return handler(events)
        return True
    
    def update(self, dt):
        """
        Update the current state.
        
        Args:
            dt: Delta time (time since last frame)
        """
        handler = self.state_handlers.get(self.current_state)
        if handler:
            handler(None, update_only=True, dt=dt)
    
    def render(self):
        """
        Render the current state.
        """
        handler = self.state_handlers.get(self.current_state)
        if handler:
            handler(None, render_only=True)
    
    def _handle_menu_state(self, events=None, update_only=False, render_only=False, dt=0):
        """Handle MENU state events and rendering."""
        if render_only:
            if self.menu_handler:
                self.menu_handler.render(self.screen)
            return True
        
        if update_only:
            if self.menu_handler:
                self.menu_handler.update(dt)
            return True
        
        # Handle events
        if events and self.menu_handler:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        selected_game = self.menu_handler.get_selected_option()
                        if selected_game == "Doom":
                            self.change_state(GameState.DOOM_GAME)
                        elif selected_game == "Contra":
                            self.change_state(GameState.CONTRA_GAME)
                        elif selected_game == "Tetris":
                            self.change_state(GameState.TETRIS_GAME)
                        elif selected_game == "Quit":
                            self.change_state(GameState.QUIT)
                
                # Let menu handle its own navigation
                self.menu_handler.handle_event(event)
        
        return True
    
    def _handle_doom_game_state(self, events=None, update_only=False, render_only=False, dt=0):
        """Handle DOOM_GAME state events and rendering."""
        if render_only:
            if self.doom_game_handler:
                self.doom_game_handler.render(self.screen)
            return True
        
        if update_only:
            if self.doom_game_handler:
                self.doom_game_handler.update(dt)
            return True
        
        # Handle events
        if events and self.doom_game_handler:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state(GameState.MENU)
                    self.doom_game_handler.handle_event(event)
        
        return True
    
    def _handle_contra_game_state(self, events=None, update_only=False, render_only=False, dt=0):
        """Handle CONTRA_GAME state events and rendering."""
        if render_only:
            if self.contra_game_handler:
                self.contra_game_handler.render(self.screen)
            return True
        
        if update_only:
            if self.contra_game_handler:
                self.contra_game_handler.update(dt)
            return True
        
        # Handle events
        if events and self.contra_game_handler:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state(GameState.MENU)
                    self.contra_game_handler.handle_event(event)
        
        return True
    
    def _handle_tetris_game_state(self, events=None, update_only=False, render_only=False, dt=0):
        """Handle TETRIS_GAME state events and rendering."""
        if render_only:
            if self.tetris_game_handler:
                self.tetris_game_handler.render(self.screen)
            return True
        
        if update_only:
            if self.tetris_game_handler:
                self.tetris_game_handler.update(dt)
            return True
        
        # Handle events
        if events and self.tetris_game_handler:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_state(GameState.MENU)
                    self.tetris_game_handler.handle_event(event)
        
        return True
    
    def _handle_quit_state(self, events=None, update_only=False, render_only=False, dt=0):
        """Handle QUIT state - should immediately quit the application."""
        print("QUIT state reached - exiting application")
        return False
    
    def get_current_state(self):
        """Get the current game state."""
        return self.current_state
    
    def is_quitting(self):
        """Check if the application should quit."""
        return self.current_state == GameState.QUIT


class BaseGameState:
    """
    Base class for all game states to inherit from.
    Provides common functionality and interface for state handlers.
    """
    
    def __init__(self):
        """Initialize the base game state."""
        self.screen = None
        self.clock = None
        self.animation_time = 0.0
    
    def set_screen_and_clock(self, screen, clock):
        """
        Set the screen and clock for this state.
        
        Args:
            screen: Pygame surface for rendering
            clock: Pygame clock for timing
        """
        self.screen = screen
        self.clock = clock
    
    def handle_event(self, event):
        """
        Handle a single Pygame event.
        
        Args:
            event: Pygame event to handle
            
        Returns:
            bool: True if event was handled, False otherwise
        """
        return False
    
    def update(self, dt):
        """
        Update the game state.
        
        Args:
            dt: Delta time (time since last frame)
        """
        self.animation_time += dt
    
    def render(self, screen):
        """
        Render the game state.
        
        Args:
            screen: Pygame surface to render to
        """
        pass