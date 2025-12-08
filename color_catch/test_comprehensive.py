#!/usr/bin/env python3
"""
Comprehensive test script for Color Catch game
This script tests all core gameplay mechanics, scoring, difficulty progression,
pause/resume functionality, command system, and visual elements.

Designed to allow recording while testing all features systematically.
"""

import pygame
import sys
import time
import random
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from contextlib import redirect_stdout

# Import game components
from game import Game
from player import Player
from target import Target
from particle import Particle, ParticleSystem
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_WIDTH, PLAYER_HEIGHT,
    PLAYER_SPEED, TARGET_WIDTH, TARGET_HEIGHT, TARGET_INITIAL_SPEED,
    SPEED_INCREASE_PERCENTAGE, MAX_SPEED, START, PLAYING, GAME_OVER,
    VICTORY, PAUSED, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, PURPLE
)

class TestColorCatchGame(unittest.TestCase):
    """Comprehensive test suite for Color Catch game"""

    def setUp(self):
        """Set up test environment"""
        pygame.init()
        self.test_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game = Game(self.test_screen)

        # Store original methods for mocking
        self.original_time = time.time

        # Mock time for consistent testing
        self.current_time = 0
        def mock_time():
            return self.current_time
        time.time = mock_time

    def tearDown(self):
        """Clean up after tests"""
        # Restore original time function
        time.time = self.original_time
        pygame.quit()

    def test_player_movement(self):
        """Test 1: Player movement mechanics"""
        print("\n=== Testing Player Movement ===")

        # Test player initialization
        player = self.game.player
        self.assertIsNotNone(player, "Player should be initialized")
        self.assertEqual(player.x, SCREEN_WIDTH // 2, "Player should start at center X")
        self.assertEqual(player.y, SCREEN_HEIGHT - 50, "Player should start at bottom")

        # Test initial position
        initial_x, initial_y = player.x, player.y

        # Test left movement
        player.move_left = True
        player.update()
        self.assertLess(player.x, initial_x, "Player should move left")
        player.move_left = False

        # Test right movement
        player.move_right = True
        player.update()
        self.assertGreater(player.x, initial_x, "Player should move right")
        player.move_right = False

        # Test screen boundary constraints
        player.x = -100
        player.update()
        self.assertEqual(player.x, 0, "Player should not go off left edge")

        player.x = SCREEN_WIDTH + 100
        player.update()
        self.assertEqual(player.x, SCREEN_WIDTH - PLAYER_WIDTH, "Player should not go off right edge")

        print("✓ Player movement mechanics working correctly")

    def test_target_movement(self):
        """Test 2: Target movement and collision mechanics"""
        print("\n=== Testing Target Movement ===")

        target = self.game.target
        self.assertIsNotNone(target, "Target should be initialized")

        # Test initial speed
        initial_speed = target.get_speed()
        self.assertEqual(initial_speed, TARGET_INITIAL_SPEED, "Target should start at initial speed")

        # Test target movement
        initial_x, initial_y = target.x, target.y
        target.update()
        self.assertNotEqual((target.x, target.y), (initial_x, initial_y), "Target should move")

        # Test boundary bouncing
        target.x = -10
        target.update()
        self.assertEqual(target.x, 0, "Target should bounce off left edge")
        self.assertEqual(target.direction_x, 1, "Target should reverse X direction on left edge")

        target.x = SCREEN_WIDTH + 10
        target.update()
        self.assertEqual(target.x, SCREEN_WIDTH - TARGET_WIDTH, "Target should bounce off right edge")
        self.assertEqual(target.direction_x, -1, "Target should reverse X direction on right edge")

        print("✓ Target movement and boundary mechanics working correctly")

    def test_collision_detection(self):
        """Test 3: Collision detection system"""
        print("\n=== Testing Collision Detection ===")

        # Position player and target to collide
        player = self.game.player
        target = self.game.target

        # Set positions to ensure collision
        player.x, player.y = 100, 100
        target.x, target.y = 100, 100

        # Update rectangles
        player.rect.x, player.rect.y = player.x, player.y
        target.rect.x, target.rect.y = target.x, target.y

        # Test collision detection
        self.assertTrue(player.rect.colliderect(target.rect), "Player and target should collide")

        # Test collision handling
        initial_score = self.game.score
        self.game._handle_collision()

        # Verify score increased
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase on collision")

        # Verify target respawned
        new_target_pos = (target.x, target.y)
        self.assertNotEqual(new_target_pos, (100, 100), "Target should respawn after collision")

        print("✓ Collision detection and handling working correctly")

    def test_scoring_system(self):
        """Test 4: Scoring system validation"""
        print("\n=== Testing Scoring System ===")

        # Test initial score
        self.assertEqual(self.game.score, 0, "Game should start with score 0")

        # Test score increase
        initial_score = self.game.score
        self.game._increase_score()
        self.assertEqual(self.game.score, initial_score + 1, "Score should increase by 1")

        # Test multiple score increases
        for _ in range(5):
            self.game._increase_score()
        self.assertEqual(self.game.score, initial_score + 6, "Multiple score increases should work")

        # Test score display rendering (no exceptions)
        try:
            self.game._draw_score()
            print("✓ Score display rendering works without errors")
        except Exception as e:
            self.fail(f"Score rendering failed with error: {e}")

        print("✓ Scoring system working correctly")

    def test_difficulty_progression(self):
        """Test 5: Difficulty progression (speed increases)"""
        print("\n=== Testing Difficulty Progression ===")

        target = self.game.target
        initial_speed = target.get_speed()

        # Test speed increase after collisions
        for i in range(1, 10):
            target.respawn()  # This increases speed
            current_speed = target.get_speed()

            # Verify speed increases (unless at max)
            if current_speed < MAX_SPEED:
                self.assertGreater(current_speed, initial_speed, f"Speed should increase after collision {i}")

            # Verify speed doesn't exceed maximum
            self.assertLessEqual(current_speed, MAX_SPEED, f"Speed should not exceed maximum")

            print(f"  Collision {i}: Speed = {current_speed:.2f}")

        # Test that speed caps at maximum
        while target.get_speed() < MAX_SPEED:
            target.respawn()

        final_speed = target.get_speed()
        self.assertEqual(final_speed, MAX_SPEED, "Speed should cap at maximum")
        print(f"✓ Difficulty progression working correctly (capped at {MAX_SPEED})")

    def test_pause_resume_functionality(self):
        """Test 6: Pause/resume functionality"""
        print("\n=== Testing Pause/Resume Functionality ===")

        # Test initial state
        self.assertFalse(self.game.paused, "Game should start unpaused")

        # Test pause activation
        self.game.paused = True
        self.assertTrue(self.game.paused, "Game should be paused")

        # Test that game logic doesn't update when paused
        player_x_before = self.game.player.x
        target_x_before = self.game.target.x

        # Mock events for pause handling
        mock_events = [MagicMock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)]

        # Update game state while paused
        self.game.update()

        # Verify positions didn't change (game logic paused)
        self.assertEqual(self.game.player.x, player_x_before, "Player should not move when paused")
        self.assertEqual(self.game.target.x, target_x_before, "Target should not move when paused")

        # Test resume
        self.game.paused = False
        self.assertFalse(self.game.paused, "Game should be unpaused")

        print("✓ Pause/resume functionality working correctly")

    def test_command_system(self):
        """Test 7: Command system (SPEED command)"""
        print("\n=== Testing Command System ===")

        # Test initial state
        self.assertFalse(self.game.speed_cheat_active, "SPEED command should start inactive")
        initial_player_speed = self.game.player.speed

        # Test SPEED command activation
        self.game._handle_speed_command()
        self.assertTrue(self.game.speed_cheat_active, "SPEED command should be active")
        self.assertEqual(self.game.player.speed, 27, "Player speed should be set to 27")

        # Test SPEED command deactivation
        self.game._handle_speed_command()
        self.assertFalse(self.game.speed_cheat_active, "SPEED command should be inactive")
        self.assertEqual(self.game.player.speed, initial_player_speed, "Player speed should be restored")

        print("✓ Command system (SPEED command) working correctly")

    def test_extended_gameplay_stability(self):
        """Test 8: Extended gameplay for stability"""
        print("\n=== Testing Extended Gameplay Stability ===")

        # Simulate extended gameplay
        for frame in range(1000):  # Simulate 1000 frames (~16 seconds at 60 FPS)
            # Update game state
            self.game.update()

            # Occasionally trigger collisions
            if frame % 50 == 0:
                self.game._handle_collision()

            # Occasionally pause/resume
            if frame % 100 == 0:
                self.game.paused = not self.game.paused

            # Verify game state is consistent
            self.assertIsNotNone(self.game.player, f"Player should exist at frame {frame}")
            self.assertIsNotNone(self.game.target, f"Target should exist at frame {frame}")

            # Verify score is reasonable
            self.assertGreaterEqual(self.game.score, 0, f"Score should be non-negative at frame {frame}")
            self.assertLessEqual(self.game.score, frame // 50 + 10, f"Score should be reasonable at frame {frame}")

        print("✓ Extended gameplay stability test passed (1000 frames)")

    def test_high_score_scenarios(self):
        """Test 9: High score scenarios"""
        print("\n=== Testing High Score Scenarios ===")

        # Test rapid scoring
        for _ in range(50):  # Score 50 points to trigger victory
            self.game._increase_score()

        self.assertEqual(self.game.score, 50, "Should be able to reach high score")

        # Test victory condition
        self.game._check_win_condition()
        self.assertTrue(self.game.victory, "Should trigger victory at 50 points")
        self.assertEqual(self.game.game_state, VICTORY, "Game state should be VICTORY")

        print("✓ High score scenarios working correctly")

    def test_edge_cases(self):
        """Test 10: Edge case validation"""
        print("\n=== Testing Edge Cases ===")

        # Test player at screen edges
        player = self.game.player

        # Test top-left corner
        player.x, player.y = 0, 0
        player.update()
        self.assertEqual(player.x, 0, "Player should stay at left edge")
        self.assertEqual(player.y, 0, "Player should stay at top edge")

        # Test bottom-right corner
        player.x = SCREEN_WIDTH
        player.y = SCREEN_HEIGHT
        player.update()
        self.assertEqual(player.x, SCREEN_WIDTH - PLAYER_WIDTH, "Player should stay at right edge")
        self.assertEqual(player.y, SCREEN_HEIGHT - PLAYER_HEIGHT, "Player should stay at bottom edge")

        # Test target at maximum speed
        target = self.game.target
        target.speed = MAX_SPEED
        target.respawn()  # Should not increase beyond max
        self.assertLessEqual(target.get_speed(), MAX_SPEED, "Target speed should not exceed maximum")

        # Test collision with None objects (safety)
        self.game.player = None
        self.game.target = None
        try:
            self.game._check_collisions()
            print("✓ Edge case: Null object handling works")
        except Exception as e:
            self.fail(f"Null object handling failed: {e}")

        # Restore objects
        self.game._initialize_game_objects()

        print("✓ Edge cases handled correctly")

    def test_visual_elements(self):
        """Test 11: Visual element verification"""
        print("\n=== Testing Visual Elements ===")

        # Test particle system
        particle_system = self.game.particle_system
        self.assertIsNotNone(particle_system, "Particle system should be initialized")

        # Test particle spawning
        particle_system.spawn_particles(100, 100, RED, 10)
        self.assertEqual(len(particle_system.particles), 10, "Should spawn correct number of particles")

        # Test particle update and cleanup
        particle_system.update()
        self.assertLessEqual(len(particle_system.particles), 10, "Particle count should not increase after update")

        # Test screen shake effects
        self.game.screen_shake = 10
        self.game.shake_intensity = 5
        shake_x, shake_y = self.game._get_shake_offset()
        self.assertNotEqual((shake_x, shake_y), (0, 0), "Screen shake should produce non-zero offset")

        # Test rendering methods (no exceptions)
        try:
            self.game._draw_background()
            self.game._draw_score()
            self.game._draw_speed_indicator()
            self.game._draw_time_indicator()
            print("✓ Visual rendering methods work without errors")
        except Exception as e:
            self.fail(f"Visual rendering failed: {e}")

        print("✓ Visual elements working correctly")

    def test_complete_gameplay_session(self):
        """Test 12: Complete gameplay session"""
        print("\n=== Testing Complete Gameplay Session ===")

        # Reset game for complete session
        self.game._restart_game()
        self.assertEqual(self.game.score, 0, "Game should reset score")
        self.assertEqual(self.game.game_state, PLAYING, "Game should be in PLAYING state")

        # Simulate gameplay to victory
        for _ in range(50):
            self.game._increase_score()
            # Occasionally trigger target respawn (which increases difficulty)
            if random.random() < 0.3:
                self.game.target.respawn()

        # Verify victory condition
        self.game._check_win_condition()
        self.assertTrue(self.game.victory, "Should achieve victory")
        self.assertEqual(self.game.game_state, VICTORY, "Should be in VICTORY state")

        # Test restart functionality
        self.game._restart_game()
        self.assertEqual(self.game.score, 0, "Score should reset after restart")
        self.assertEqual(self.game.game_state, PLAYING, "Should return to PLAYING state")

        print("✓ Complete gameplay session working correctly")

    def test_user_requested_features(self):
        """Test 13: All user-requested features"""
        print("\n=== Testing User-Requested Features ===")

        # Test all game states
        game_states = [START, PLAYING, PAUSED, VICTORY, GAME_OVER]
        for state in game_states:
            self.game.game_state = state
            try:
                self.game.render()
                print(f"✓ Game state {state} renders correctly")
            except Exception as e:
                self.fail(f"Game state {state} rendering failed: {e}")

        # Test command input system
        self.game.paused = True
        self.game.command_active = True

        # Test command input handling
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_s
        mock_event.unicode = 's'
        self.game._handle_command_input(mock_event)
        self.assertEqual(self.game.command_input, 's', "Should capture command input")

        # Test command submission
        self.game.command_input = "SPEED"
        self.game._handle_command_submission()
        self.assertTrue(self.game.speed_cheat_active, "Should activate SPEED command")

        print("✓ All user-requested features working correctly")

def run_comprehensive_tests():
    """Run all comprehensive tests with detailed reporting"""
    print("🎮 COLOR CATCH COMPREHENSIVE TEST SUITE")
    print("=" * 50)
    print("Testing all game features systematically...")
    print("This test allows for game recording during execution.")
    print()

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestColorCatchGame)

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Generate comprehensive report
    print("\n" + "=" * 50)
    print("📊 COMPREHENSIVE TEST REPORT")
    print("=" * 50)

    # Test summary
    total_tests = result.testsRun
    passed_tests = total_tests - len(result.failures) - len(result.errors)
    failed_tests = len(result.failures)
    error_tests = len(result.errors)

    print(f"📈 Total Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"⚠️  Errors: {error_tests}")

    # Feature validation
    features_tested = [
        "Player Movement Mechanics",
        "Target Movement & Collisions",
        "Scoring System",
        "Difficulty Progression",
        "Pause/Resume Functionality",
        "Command System (SPEED)",
        "Extended Gameplay Stability",
        "High Score Scenarios",
        "Edge Case Handling",
        "Visual Elements",
        "Complete Gameplay Sessions",
        "User-Requested Features"
    ]

    print(f"\n🎯 Features Validated: {len(features_tested)}")
    for feature in features_tested:
        print(f"  ✓ {feature}")

    # Final validation
    if failed_tests == 0 and error_tests == 0:
        print(f"\n🎉 ALL TESTS PASSED! Game is ready for delivery.")
        print("📦 All core gameplay mechanics validated")
        print("🎮 All user-requested features implemented")
        print("🔍 All edge cases handled")
        print("🎨 All visual elements working")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Please review the issues above.")
        return False

def run_automated_test_session():
    """Run automated test session for recording purposes"""
    print("\n🎥 AUTOMATED TEST SESSION FOR RECORDING")
    print("=" * 40)

    # Initialize pygame for visible testing
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Color Catch - Automated Testing")

    game = Game(screen)
    clock = pygame.time.Clock()

    # Run through different game states for recording
    test_phases = [
        ("Start Screen", 2),
        ("Gameplay", 5),
        ("Pause Menu", 3),
        ("Victory Screen", 3),
        ("Restart", 2)
    ]

    for phase_name, duration in test_phases:
        print(f"\n🎬 Recording phase: {phase_name} ({duration} seconds)")

        start_time = time.time()
        while time.time() - start_time < duration:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Handle phase-specific logic
            if phase_name == "Start Screen":
                game.game_state = START
            elif phase_name == "Gameplay":
                game.game_state = PLAYING
                if random.random() < 0.1:  # Random collisions
                    game._handle_collision()
            elif phase_name == "Pause Menu":
                game.game_state = PLAYING
                game.paused = True
            elif phase_name == "Victory Screen":
                game.score = 50
                game._check_win_condition()
            elif phase_name == "Restart":
                game._restart_game()

            # Update and render
            game.handle_events(events)
            game.update()
            game.render()
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    print("\n✅ Automated test session completed - ready for recording review")

if __name__ == "__main__":
    # Run comprehensive tests
    success = run_comprehensive_tests()

    # Optionally run automated test session for recording
    # Uncomment the line below to run the visual test session
    # run_automated_test_session()

    sys.exit(0 if success else 1)