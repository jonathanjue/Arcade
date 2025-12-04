"""
Test script to verify the Arcade Collection components work properly.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing module imports...")
    
    try:
        import constants
        print("+ constants.py imported successfully")
        
        import game_states
        print("+ game_states.py imported successfully")
        
        import menu
        print("+ menu.py imported successfully")
        
        import games.doom
        print("+ games.doom imported successfully")
        
        import games.contra
        print("+ games.contra imported successfully")
        
        import games.tetris
        print("+ games.tetris imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"- Import error: {e}")
        return False

def test_constants():
    """Test that constants are properly defined."""
    print("\nTesting constants...")
    
    try:
        from constants import GameState, SCREEN_WIDTH, SCREEN_HEIGHT, Colors, FPS
        
        # Test game states
        expected_states = ["menu", "doom_game", "contra_game", "tetris_game", "quit"]
        for state in expected_states:
            assert hasattr(GameState, state.upper()), f"Missing state: {state}"
        
        print("+ All game states defined")
        
        # Test screen dimensions
        assert SCREEN_WIDTH == 800, f"Wrong width: {SCREEN_WIDTH}"
        assert SCREEN_HEIGHT == 600, f"Wrong height: {SCREEN_HEIGHT}"
        print("+ Screen dimensions correct")
        
        # Test colors
        assert hasattr(Colors, 'BLACK'), "Missing BLACK color"
        assert hasattr(Colors, 'WHITE'), "Missing WHITE color"
        assert hasattr(Colors, 'RED'), "Missing RED color"
        assert hasattr(Colors, 'GRAY'), "Missing GRAY color"
        print("+ Required colors defined")
        
        # Test FPS
        assert FPS == 60, f"Wrong FPS: {FPS}"
        print("+ FPS setting correct")
        
        return True
        
    except Exception as e:
        print(f"- Constants test failed: {e}")
        return False

def test_game_classes():
    """Test that game classes can be instantiated."""
    print("\nTesting game classes...")
    
    try:
        from menu import MainMenu
        from games.doom import DoomGame
        from games.contra import ContraGame
        from games.tetris import TetrisGame
        
        menu = MainMenu()
        print("+ MainMenu instantiated")
        
        doom = DoomGame()
        print("+ DoomGame instantiated")
        
        contra = ContraGame()
        print("+ ContraGame instantiated")
        
        tetris = TetrisGame()
        print("+ TetrisGame instantiated")
        
        return True
        
    except Exception as e:
        print(f"- Game class test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("ARCADE COLLECTION - Component Testing")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_constants()
    all_tests_passed &= test_game_classes()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("ALL TESTS PASSED [+]")
        print("Arcade Collection is ready to run!")
    else:
        print("SOME TESTS FAILED [-]")
        print("Please fix the issues above")
    print("=" * 50)
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)