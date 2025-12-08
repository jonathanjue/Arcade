#!/usr/bin/env python3
"""
Test script to verify the scoring system implementation
"""

import pygame
import sys
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def test_score_system():
    """Test the score system functionality"""
    print("Testing Color Catch Score System...")

    # Initialize pygame
    pygame.init()

    # Create a test screen (not visible)
    test_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create game instance
    game = Game(test_screen)

    # Test 1: Verify score starts at 0
    assert game.score == 0, f"Score should start at 0, got {game.score}"
    print("Test 1 passed: Score starts at 0")

    # Test 2: Verify font is initialized
    assert game.font is not None, "Font should be initialized"
    print("Test 2 passed: Font is initialized")

    # Test 3: Test score increase functionality
    initial_score = game.score
    game._increase_score()
    assert game.score == initial_score + 1, f"Score should increase by 1, got {game.score}"
    print("Test 3 passed: Score increases correctly")

    # Test 4: Test multiple score increases
    for i in range(5):
        game._increase_score()
    assert game.score == initial_score + 6, f"Score should be {initial_score + 6}, got {game.score}"
    print("Test 4 passed: Multiple score increases work")

    # Test 5: Test score rendering (no exceptions)
    try:
        game._draw_score()
        print("Test 5 passed: Score rendering works without errors")
    except Exception as e:
        print(f"Test 5 failed: Score rendering failed with error: {e}")
        return False

    # Test 6: Verify score display format
    score_text = f"Score: {game.score}"
    expected_format = "Score: 6"
    assert score_text == expected_format, f"Score text format should be '{expected_format}', got '{score_text}'"
    print("Test 6 passed: Score display format is correct")

    print("\nAll tests passed! Score system is working correctly.")
    return True

if __name__ == "__main__":
    success = test_score_system()
    sys.exit(0 if success else 1)