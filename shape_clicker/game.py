"""Main game class for Shape Clicker with full progression system"""

import pygame
import time
import os
from constants import *
from shapes import CircleShape, SquareShape, TriangleShape, Button
from upgrades import UpgradeSystem

# Initialize pygame mixer for music
pygame.mixer.init()


class ShapeClickerGame:
    """Main game class with full progression system"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Shape Clicker - Full Progression")
        self.clock = pygame.time.Clock()
        
        # Font setup
        self.font_small = pygame.font.Font(None, FONT_SMALL)
        self.font_medium = pygame.font.Font(None, FONT_MEDIUM)
        self.font_large = pygame.font.Font(None, FONT_LARGE)
        
        # Game state
        self.current_stage = "circle"  # "circle", "square", "triangle", "victory"
        self.circle_points = STARTING_CIRCLE_POINTS  # Start with 100 points
        self.square_points = 0
        self.triangle_points = 0
        
        # Cheat mode and special features
        self.cheat_mode = False
        self.cheat_buffer = ""
        self.timewarp_mode = False
        self.current_music = None
        self.music_buttons = {}
        self.music_playing = False
        
        # Powerup system
        self.auto_clicker_helper_active = False
        self.click_power_helper_active = False
        self.auto_clicker_helper_end_time = 0
        self.click_power_helper_end_time = 0
        self.auto_clicker_helper_cost = 0
        self.click_power_helper_cost = 0
        
        # Color system
        self.current_shape_color = None
        
        # Expert mode
        self.expert_mode_unlocked = False
        self.expert_mode_active = False
        
        # Compound stage
        self.compound_points = 0
        self.total_compound_points = 0
        
        # Progression tracking
        self.total_circle_points = 0
        self.total_square_points = 0
        self.total_triangle_points = 0
        self.game_start_time = time.time()
        
        # Transition messages
        self.show_transition = False
        self.transition_message = ""
        self.transition_start_time = 0
        self.transition_duration = 3.0  # 3 seconds
        
        # Victory state
        self.victory_time = 0
        
        # Achievement state
        self.victory_achievements = []
        self.show_achievements = False
        self.achievement_start_time = 0
        
        # Game objects
        self.upgrades = UpgradeSystem()
        self.upgrades.set_stage("circle")  # Initialize for circle stage
        
        # Shape objects
        self.circle = CircleShape(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.square = SquareShape(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.triangle = TriangleShape(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # UI buttons
        self.click_power_button = Button(
            UI_PADDING,
            SCREEN_HEIGHT // 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Click Power"
        )
        
        self.auto_clicker_button = Button(
            UI_PADDING,
            SCREEN_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_SPACING,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Auto Clicker"
        )
        
        # Victory restart button (initially hidden)
        self.restart_button = Button(
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2 + 100,
            200,
            60,
            "Play Again"
        )
        
        # Auto clicker timer
        self.last_auto_click_time = time.time()
        
    def handle_events(self):
        """Handle pygame events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Handle cheat input
                if event.key == pygame.K_BACKSPACE:
                    self.cheat_buffer = self.cheat_buffer[:-1]
                elif event.key == pygame.K_RETURN:
                    command = self.cheat_buffer.lower()
                    if command == "cheat":
                        self.cheat_mode = not self.cheat_mode
                        print(f"Cheat mode {'enabled' if self.cheat_mode else 'disabled'}!")
                    elif command == "timewarp":
                        self.timewarp_mode = not self.timewarp_mode
                        print(f"Timewarp mode {'enabled' if self.timewarp_mode else 'disabled'}!")
                    elif command in MUSIC_FILES:
                        music_name = command
                        if music_name not in self.music_buttons:
                            # Create music button for this track - position around screen
                            button_positions = {
                                'loonboon': (SCREEN_WIDTH - MUSIC_BUTTON_WIDTH - 50, 50),  # Top right
                                'doometernal': (50, 50),  # Top left
                                'tetris': (SCREEN_WIDTH - MUSIC_BUTTON_WIDTH - 50, SCREEN_HEIGHT - MUSIC_BUTTON_HEIGHT - 50),  # Bottom right
                                'coin': (50, SCREEN_HEIGHT - MUSIC_BUTTON_HEIGHT - 50),  # Bottom left
                            }
                            
                            if music_name in button_positions:
                                button_x, button_y = button_positions[music_name]
                            else:
                                button_x = (SCREEN_WIDTH - MUSIC_BUTTON_WIDTH) // 2
                                button_y = MUSIC_BUTTON_Y_START
                            
                            button_y = MUSIC_BUTTON_Y_START
                            if music_name in button_positions:
                                button_y = button_positions[music_name][1]
                            
                            self.music_buttons[music_name] = {
                                'button': Button(button_x, button_y, MUSIC_BUTTON_WIDTH, MUSIC_BUTTON_HEIGHT, MUSIC_NAMES[music_name]),
                                'file': MUSIC_FILES[music_name]
                            }
                            print(f"Added {MUSIC_NAMES[music_name]} toggle!")
                    
                    # Color commands
                    elif command in SHAPE_COLORS:
                        color_name = command
                        self.current_shape_color = SHAPE_COLORS[color_name]
                        print(f"Shape color changed to {color_name}!")
                    
                    # Expert mode unlock
                    elif command == "expert" and self.expert_mode_unlocked:
                        self.expert_mode_active = not self.expert_mode_active
                        print(f"Expert mode {'enabled' if self.expert_mode_active else 'disabled'}!")
                        
                        # Reset upgrades for expert mode
                        if self.expert_mode_active:
                            self.upgrades.reset()
                            self.upgrades.set_stage(self.current_stage)
                            if self.current_stage == "circle":
                                self.circle_points = STARTING_CIRCLE_POINTS
                            elif self.current_stage == "square":
                                self.square_points = 0
                            elif self.current_stage == "triangle":
                                self.triangle_points = 0
                    
                    self.cheat_buffer = ""
                else:
                    self.cheat_buffer += event.unicode
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(mouse_pos)
        
        # Update button states
        if self.current_stage != "victory":
            self.click_power_button.update_state(mouse_pos)
            self.auto_clicker_button.update_state(mouse_pos)
        else:
            self.restart_button.update_state(mouse_pos)
        
        # Update music button states
        for music_data in self.music_buttons.values():
            music_data['button'].update_state(mouse_pos)
        
        return True
    
    def handle_click(self, mouse_pos):
        """Handle click events"""
        if self.current_stage == "victory":
            # Handle restart button
            if self.restart_button.is_clicked(mouse_pos):
                self.restart_game()
            return
        
        current_points = self.get_current_points()
        
        # Check if shape was clicked
        current_shape = self.get_current_shape()
        if current_shape.update_highlight(mouse_pos) and current_shape.is_clicked(mouse_pos):
            if self.cheat_mode:
                # Cheat mode: add 1000 points
                click_power = 1000
            else:
                click_power = self.upgrades.get_click_power()
                self.upgrades.used_manual_clicking = True  # Track for ROBOT achievement
            
            if self.current_stage == "circle":
                self.circle_points += click_power
            elif self.current_stage == "square":
                self.square_points += click_power
            elif self.current_stage == "triangle":
                self.triangle_points += click_power
        
        # Check if upgrade buttons were clicked
        if self.click_power_button.is_clicked(mouse_pos):
            success, new_points = self.upgrades.buy_click_power(current_points)
            if success:
                self.upgrades.record_upgrade_usage('click_power')  # Track achievement
                if self.current_stage == "circle":
                    self.circle_points = new_points
                elif self.current_stage == "square":
                    self.square_points = new_points
                elif self.current_stage == "triangle":
                    self.triangle_points = new_points
        
        # Check if music buttons were clicked
        for music_name, music_data in self.music_buttons.items():
            if music_data['button'].is_clicked(mouse_pos):
                self.toggle_music(music_name)
    
    def toggle_music(self, music_name):
        """Toggle music for a specific track"""
        if self.current_music == music_name:
            # Stop current music
            pygame.mixer.music.stop()
            self.current_music = None
            self.music_playing = False
            print(f"Stopped {MUSIC_NAMES[music_name]}")
        else:
            # Start new music
            music_file = self.music_buttons[music_name]['file']
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = music_name
                self.music_playing = True
                print(f"Started {MUSIC_NAMES[music_name]}")
            except pygame.error:
                print(f"Could not load music file: {music_file}")
                print("Make sure the music files are in the game directory.")
        
        if self.auto_clicker_button.is_clicked(mouse_pos):
            success, new_points = self.upgrades.buy_auto_clicker(current_points)
            if success:
                self.upgrades.record_upgrade_usage('auto_clicker')  # Track achievement
                if self.current_stage == "circle":
                    self.circle_points = new_points
                elif self.current_stage == "square":
                    self.square_points = new_points
                elif self.current_stage == "triangle":
                    self.triangle_points = new_points
        
        # Check if music buttons were clicked
        for music_name, music_data in self.music_buttons.items():
            if music_data['button'].is_clicked(mouse_pos):
                self.toggle_music(music_name)
    
    def toggle_music(self, music_name):
        """Toggle music for a specific track"""
        if self.current_music == music_name:
            # Stop current music
            pygame.mixer.music.stop()
            self.current_music = None
            self.music_playing = False
            print(f"Stopped {MUSIC_NAMES[music_name]}")
        else:
            # Start new music
            music_file = self.music_buttons[music_name]['file']
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = music_name
                self.music_playing = True
                print(f"Started {MUSIC_NAMES[music_name]}")
            except pygame.error:
                print(f"Could not load music file: {music_file}")
                print("Make sure the music files are in the game directory.")
        
        # Check if music buttons were clicked
        for music_name, music_data in self.music_buttons.items():
            if music_data['button'].is_clicked(mouse_pos):
                self.toggle_music(music_name)
    
    def toggle_music(self, music_name):
        """Toggle music for a specific track"""
        if self.current_music == music_name:
            # Stop current music
            pygame.mixer.music.stop()
            self.current_music = None
            self.music_playing = False
            print(f"Stopped {MUSIC_NAMES[music_name]}")
        else:
            # Start new music
            music_file = self.music_buttons[music_name]['file']
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.current_music = music_name
                self.music_playing = True
                print(f"Started {MUSIC_NAMES[music_name]}")
            except pygame.error:
                print(f"Could not load music file: {music_file}")
                print("Make sure the music files are in the game directory.")
    
    def get_current_shape(self):
        """Get the current active shape"""
        if self.current_stage == "circle":
            return self.circle
        elif self.current_stage == "square":
            return self.square
        elif self.current_stage == "triangle":
            return self.triangle
        else:  # victory stage
            return None
    
    def get_current_points(self):
        """Get current points based on stage"""
        if self.current_stage == "circle":
            return self.circle_points
        elif self.current_stage == "square":
            return self.square_points
        elif self.current_stage == "triangle":
            return self.triangle_points
        else:
            return 0
    
    def restart_game(self):
        """Restart the game to initial state"""
        self.current_stage = "circle"
        self.circle_points = STARTING_CIRCLE_POINTS  # Start with 100 points
        self.square_points = 0
        self.triangle_points = 0
        
        # Reset progression tracking
        self.total_circle_points = 0
        self.total_square_points = 0
        self.total_triangle_points = 0
        
        # Reset upgrades and stage
        self.upgrades = UpgradeSystem()
        self.upgrades.set_stage("circle")
        
        # Reset timers and transitions
        self.game_start_time = time.time()
        self.show_transition = False
        self.victory_time = 0
        
        # Reset achievement tracking
        self.victory_achievements = []
        self.show_achievements = False
        self.achievement_start_time = 0
        
        # Reset cheat mode and features
        self.cheat_mode = False
        self.cheat_buffer = ""
        self.timewarp_mode = False
        self.current_music = None
        self.music_buttons = {}
        self.music_playing = False
        
        # Stop any playing music
        pygame.mixer.music.stop()
    
    def update_auto_clicks(self):
        """Update auto clicker points"""
        if self.current_stage == "victory":
            return
            
        current_time = time.time()
        if current_time - self.last_auto_click_time >= 1.0:  # 1 second
            points_per_second = self.upgrades.get_points_per_second()
            # Apply timewarp multiplier if enabled
            if self.timewarp_mode:
                points_per_second *= TIMEWARP_MULTIPLIER
            
            if points_per_second > 0:
                if self.current_stage == "circle":
                    self.circle_points += points_per_second
                elif self.current_stage == "square":
                    self.square_points += points_per_second
                elif self.current_stage == "triangle":
                    self.triangle_points += points_per_second
                self.last_auto_click_time = current_time
    
    def check_stage_progression(self):
        """Check if stage should progress"""
        if self.current_stage == "circle" and self.circle_points >= CIRCLE_MAX_POINTS:
            # Progress to square stage
            self.current_stage = "square"
            self.total_circle_points += self.circle_points
            self.circle_points = 0
            
            # Apply multiplier if auto clickers were used
            had_auto_clicker = self.upgrades.auto_clicker_level > 0
            multiplier_applied = self.upgrades.advance_stage(had_auto_clicker)
            
            self.upgrades.reset()
            self.upgrades.set_stage("square")
            self.show_transition = True
            self.transition_message = "Circle to Square Progress!" + (" (+1.25x Bonus!)" if multiplier_applied else "")
            self.transition_start_time = time.time()
            print("Progressed to Square Stage!" + (" with multiplier!" if multiplier_applied else ""))
            
        elif self.current_stage == "square" and self.square_points >= SQUARE_MAX_POINTS:
            # Progress to triangle stage
            self.current_stage = "triangle"
            self.total_square_points += self.square_points
            self.square_points = 0
            
            # Apply multiplier if auto clickers were used
            had_auto_clicker = self.upgrades.auto_clicker_level > 0
            multiplier_applied = self.upgrades.advance_stage(had_auto_clicker)
            
            self.upgrades.reset()
            self.upgrades.set_stage("triangle")
            self.show_transition = True
            self.transition_message = "Square to Triangle Progress!" + (" (+1.25x Bonus!)" if multiplier_applied else "")
            self.transition_start_time = time.time()
            print("Progressed to Triangle Stage!" + (" with multiplier!" if multiplier_applied else ""))
            
            # Add boss music button for triangle stage
            if 'boss' not in self.music_buttons:
                self.music_buttons['boss'] = {
                    'button': Button((SCREEN_WIDTH - MUSIC_BUTTON_WIDTH) // 2, SCREEN_HEIGHT - MUSIC_BUTTON_HEIGHT - 50, MUSIC_BUTTON_WIDTH, MUSIC_BUTTON_HEIGHT, MUSIC_NAMES['boss']),
                    'file': MUSIC_FILES['boss']
                }
                print("Boss music button unlocked!")
            
        elif self.current_stage == "triangle" and self.triangle_points >= TRIANGLE_MAX_POINTS:
            # Victory condition reached
            self.current_stage = "victory"
            self.total_triangle_points += self.triangle_points
            self.triangle_points = 0
            self.victory_time = time.time()
            
            # Play victory music
            self.play_victory_music()
            
            # Check for achievements
            achievements = self.upgrades.check_achievement_criteria()
            self.victory_achievements = []
            
            if achievements['pure_clicker']:
                self.victory_achievements.append({
                    'name': ACHIEVEMENT_PURE_CLICKER,
                    'description': ACHIEVEMENT_PURE_CLICKER_DESC
                })
                
            if achievements['auto_master']:
                self.victory_achievements.append({
                    'name': ACHIEVEMENT_AUTO_MASTER,
                    'description': ACHIEVEMENT_AUTO_MASTER_DESC
                })
                
            if achievements['robot']:
                self.victory_achievements.append({
                    'name': ACHIEVEMENT_ROBOT,
                    'description': ACHIEVEMENT_ROBOT_DESC
                })
            
            # Show achievements after victory
            if self.victory_achievements:
                self.show_achievements = True
                self.achievement_start_time = time.time()
            
            print("You Win! Congratulations!")
            print(f"Achievements earned: {[ach['name'] for ach in self.victory_achievements]}")
        
        # Hide transition message after duration
        if self.show_transition and time.time() - self.transition_start_time >= self.transition_duration:
            self.show_transition = False
    
    def draw_ui(self):
        """Draw the user interface"""
        mouse_pos = pygame.mouse.get_pos()
        
        if self.current_stage == "victory":
            self.draw_victory_screen()
            return
        
        current_points = self.get_current_points()
        
        # Draw title
        stage_titles = {
            "circle": "Circle Stage",
            "square": "Square Stage", 
            "triangle": "Triangle Stage"
        }
        stage_text = stage_titles.get(self.current_stage, "Unknown Stage")
        title_surface = self.font_large.render(stage_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title_surface, title_rect)
        
        # Show timewarp mode status (hidden cheat)
        if self.timewarp_mode:
            timewarp_surface = self.font_small.render("TIMEWARP MODE: ON", True, YELLOW)
            timewarp_rect = timewarp_surface.get_rect(topleft=(10, 10))
            self.screen.blit(timewarp_surface, timewarp_rect)
        
        # Show cheat input buffer (hidden)
        if self.cheat_buffer:
            cheat_input = f"Input: {self.cheat_buffer}_"
            cheat_input_surface = self.font_small.render(cheat_input, True, WHITE)
            cheat_input_rect = cheat_input_surface.get_rect(topleft=(10, 30))
            self.screen.blit(cheat_input_surface, cheat_input_rect)
        
        # Draw progress bar
        max_points = {
            "circle": CIRCLE_MAX_POINTS,
            "square": SQUARE_MAX_POINTS,
            "triangle": TRIANGLE_MAX_POINTS
        }
        
        current_max = max_points.get(self.current_stage, 10000)
        progress = min(current_points / current_max, 1.0)
        bar_width = 400
        bar_height = 20
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 60
        
        # Draw progress bar background
        pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Draw progress bar fill
        progress_color = BLUE if self.current_stage == "circle" else (RED if self.current_stage == "square" else GREEN)
        pygame.draw.rect(self.screen, progress_color, (bar_x, bar_y, bar_width * progress, bar_height))
        # Draw progress bar border
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw points
        points_text = f"Points: {current_points:,}"
        if self.current_stage != "triangle":
            points_text += f" / {current_max:,}"
        else:
            points_text += f" / {current_max:,} (VICTORY!)"
            
        points_surface = self.font_medium.render(points_text, True, YELLOW)
        points_rect = points_surface.get_rect(center=(SCREEN_WIDTH // 2, 90))
        self.screen.blit(points_surface, points_rect)
        
        # Draw points per second
        pps = self.upgrades.get_points_per_second()
        pps_text = f"Points per second: {pps}"
        pps_surface = self.font_small.render(pps_text, True, WHITE)
        pps_rect = pps_surface.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(pps_surface, pps_rect)
        
        # Draw upgrade stats
        stats = self.upgrades.get_stats_text()
        stats_texts = [
            f"Click Power: {stats['current_click_power']} (Level {stats['click_power_level']})",
            f"Auto Clicker: {stats['current_points_per_second']} (Level {stats['auto_clicker_level']})"
        ]
        
        for i, text in enumerate(stats_texts):
            stat_surface = self.font_small.render(text, True, LIGHT_GRAY)
            stat_rect = stat_surface.get_rect(center=(SCREEN_WIDTH // 2, 160 + i * 25))
            self.screen.blit(stat_surface, stat_rect)
        
        # Update button costs and enabled states
        self.click_power_button.cost = stats['click_power_cost']
        self.auto_clicker_button.cost = stats['auto_clicker_cost']
        
        self.click_power_button.enabled = current_points >= stats['click_power_cost']
        self.auto_clicker_button.enabled = current_points >= stats['auto_clicker_cost']
        
        # Draw upgrade buttons
        self.click_power_button.draw(self.screen, self.font_small)
        self.auto_clicker_button.draw(self.screen, self.font_small)
        
        # Draw music buttons if any
        for music_name, music_data in self.music_buttons.items():
            button = music_data['button']
            # Update button appearance based on whether music is playing
            button.enabled = True  # Music buttons are always enabled
            button.clicked = (self.current_music == music_name and self.music_playing)
            button.draw(self.screen, self.font_small)
        
        # Draw progression tracking
        if self.current_stage in ["square", "triangle"]:
            prog_texts = [
                f"Circle Points Earned: {self.total_circle_points:,}",
                f"Square Points Earned: {self.total_square_points:,}"
            ]
            
            if self.current_stage == "triangle":
                prog_texts.append(f"Triangle Points Earned: {self.total_triangle_points:,}")
                
            for i, text in enumerate(prog_texts):
                prog_surface = self.font_small.render(text, True, GREEN)
                prog_rect = prog_surface.get_rect(center=(SCREEN_WIDTH // 2, 280 + i * 25))
                self.screen.blit(prog_surface, prog_rect)
        
        # Draw transition message
        if self.show_transition:
            self.draw_transition_message()
    
    def draw_transition_message(self):
        """Draw transition message with fade effect"""
        current_time = time.time()
        elapsed = current_time - self.transition_start_time
        
        # Fade in and out effect
        if elapsed < 0.5:
            alpha = int(255 * (elapsed / 0.5))  # Fade in
        elif elapsed > self.transition_duration - 0.5:
            alpha = int(255 * ((self.transition_duration - elapsed) / 0.5))  # Fade out
        else:
            alpha = 255  # Full opacity
        
        # Create text surface with alpha
        message_surface = self.font_large.render(self.transition_message, True, YELLOW)
        message_surface.set_alpha(alpha)
        
        # Center the message
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(message_surface, message_rect)
        
        # Draw additional celebration text
        if "Square" in self.transition_message:
            celebration_text = "New shape unlocked!"
        elif "Triangle" in self.transition_message:
            celebration_text = "Final stage unlocked!"
        else:
            celebration_text = "Congratulations!"
            
        celebration_surface = self.font_medium.render(celebration_text, True, WHITE)
        celebration_surface.set_alpha(alpha)
        celebration_rect = celebration_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(celebration_surface, celebration_rect)
    
    def draw_victory_screen(self):
        """Draw the victory screen"""
        # Clear background with a gradient effect
        for i in range(SCREEN_HEIGHT):
            color_ratio = i / SCREEN_HEIGHT
            r = int(50 + color_ratio * 100)  # Dark to lighter
            g = int(150 + color_ratio * 105)  # Green gradient
            b = int(50 + color_ratio * 100)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))
        
        # Draw "YOU WIN!" title
        win_surface = self.font_large.render("YOU WIN!", True, YELLOW)
        win_rect = win_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Add glow effect
        for offset in range(3, 0, -1):
            glow_surface = self.font_large.render("YOU WIN!", True, (255, 255, 0))
            glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH // 2 + offset, 150 + offset))
            self.screen.blit(glow_surface, glow_rect)
        
        self.screen.blit(win_surface, win_rect)
        
        # Draw final statistics
        total_time = self.victory_time - self.game_start_time
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
        
        # Draw multiplier information if applied
        multiplier_info = self.upgrades.get_multiplier_info()
        stats_texts = [
            f"Final Statistics:",
            f"Circle Points Earned: {self.total_circle_points:,}",
            f"Square Points Earned: {self.total_square_points:,}",
            f"Triangle Points Earned: {self.total_triangle_points:,}",
            f"Total Time: {minutes}:{seconds:02d}"
        ]
        
        # Add multiplier info if any was applied
        if multiplier_info['stages_with_multiplier'] > 0:
            stats_texts.append(f"Stage Bonus Applied: {multiplier_info['current_multiplier']:.2f}x")
        
        stats_texts.append(f"Congratulations on completing the challenge!")
        
        for i, text in enumerate(stats_texts):
            if i == 0:  # Title
                stat_surface = self.font_medium.render(text, True, WHITE)
            else:
                stat_surface = self.font_small.render(text, True, LIGHT_GRAY)
            stat_rect = stat_surface.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 30))
            self.screen.blit(stat_surface, stat_rect)
        
        # Draw achievements if any were earned
        if self.victory_achievements:
            ach_y_start = 250 + len(stats_texts) * 30 + 50
            
            ach_title = "ACHIEVEMENTS UNLOCKED!"
            ach_title_surface = self.font_medium.render(ach_title, True, ACHIEVEMENT_GOLD)
            ach_title_rect = ach_title_surface.get_rect(center=(SCREEN_WIDTH // 2, ach_y_start))
            self.screen.blit(ach_title_surface, ach_title_rect)
            
            for i, achievement in enumerate(self.victory_achievements):
                ach_text = f"🏆 {achievement['name']}"
                ach_desc = achievement['description']
                
                ach_text_surface = self.font_small.render(ach_text, True, ACHIEVEMENT_GOLD)
                ach_desc_surface = self.font_small.render(ach_desc, True, WHITE)
                
                ach_y = ach_y_start + 40 + i * 50
                ach_rect = ach_text_surface.get_rect(center=(SCREEN_WIDTH // 2, ach_y))
                ach_desc_rect = ach_desc_surface.get_rect(center=(SCREEN_WIDTH // 2, ach_y + 25))
                
                self.screen.blit(ach_text_surface, ach_rect)
                self.screen.blit(ach_desc_surface, ach_desc_rect)
        
        # Draw music buttons on victory screen too
        for music_name, music_data in self.music_buttons.items():
            button = music_data['button']
            button.enabled = True
            button.clicked = (self.current_music == music_name and self.music_playing)
            button.draw(self.screen, self.font_small)
        
        # Draw restart button
        self.restart_button.draw(self.screen, self.font_small)
        
        # Draw victory message
        victory_msg = "Click 'Play Again' to restart your journey!"
        msg_surface = self.font_small.render(victory_msg, True, YELLOW)
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, 550))
        self.screen.blit(msg_surface, msg_rect)
    
    def draw(self):
        """Draw the game"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw current shape (skip if in victory stage)
        if self.current_stage != "victory":
            current_shape = self.get_current_shape()
            if current_shape:
                current_shape.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw achievements if being shown
        if self.show_achievements:
            self.draw_achievement_notifications()
        
        # Update display
        pygame.display.flip()
    
    def draw_achievement_notifications(self):
        """Draw achievement notifications with gold fade effect"""
        current_time = time.time()
        elapsed = current_time - self.achievement_start_time
        
        if elapsed >= ACHIEVEMENT_FADE_DURATION:
            self.show_achievements = False
            return
        
        # Calculate fade effect (same as transition message)
        if elapsed < 0.5:
            alpha = int(255 * (elapsed / 0.5))  # Fade in
        elif elapsed > ACHIEVEMENT_FADE_DURATION - 0.5:
            alpha = int(255 * ((ACHIEVEMENT_FADE_DURATION - elapsed) / 0.5))  # Fade out
        else:
            alpha = 255  # Full opacity
        
        # Draw each achievement as a golden notification
        ach_start_y = SCREEN_HEIGHT // 2 - len(self.victory_achievements) * 30
        
        for i, achievement in enumerate(self.victory_achievements):
            # Achievement name in gold
            ach_name = f"🏆 ACHIEVEMENT UNLOCKED: {achievement['name']}"
            name_surface = self.font_medium.render(ach_name, True, ACHIEVEMENT_GOLD)
            name_surface.set_alpha(alpha)
            name_rect = name_surface.get_rect(center=(SCREEN_WIDTH // 2, ach_start_y + i * 60))
            
            # Achievement description in white
            desc_surface = self.font_small.render(achievement['description'], True, WHITE)
            desc_surface.set_alpha(alpha)
            desc_rect = desc_surface.get_rect(center=(SCREEN_WIDTH // 2, ach_start_y + i * 60 + 25))
            
            self.screen.blit(name_surface, name_rect)
            self.screen.blit(desc_surface, desc_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        
        # Start with game start music
        try:
            pygame.mixer.music.load(MUSIC_FILES['gamestart'])
            pygame.mixer.music.play(-1)
            self.current_music = 'gamestart'
            self.music_playing = True
            print("Game start music playing!")
        except pygame.error:
            print("Could not load game start music (gamestart.mp3)")
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update auto clicks
            self.update_auto_clicks()
            
            # Check stage progression
            self.check_stage_progression()
            
            # Draw everything
            self.draw()
            
            # Control frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def play_victory_music(self):
        """Play victory music"""
        try:
            pygame.mixer.music.load(MUSIC_FILES['ending'])
            pygame.mixer.music.play(-1)
            self.current_music = 'ending'
            self.music_playing = True
            print("Victory music playing!")
        except pygame.error:
            print("Could not load victory music (ending.mp3)")


def main():
    """Main function"""
    game = ShapeClickerGame()
    game.run()


if __name__ == "__main__":
    main()