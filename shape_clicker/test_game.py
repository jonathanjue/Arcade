#!/usr/bin/env python3
"""Test script to verify the Shape Clicker game features"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_constants():
    """Test that all constants are properly defined"""
    from constants import (
        CIRCLE_MAX_POINTS, SQUARE_MAX_POINTS, TRIANGLE_MAX_POINTS,
        CIRCLE_CLICK_POWER_BASE_COST, SQUARE_CLICK_POWER_BASE_COST, TRIANGLE_CLICK_POWER_BASE_COST,
        CIRCLE_AUTO_CLICKER_BASE_COST, SQUARE_AUTO_CLICKER_BASE_COST, TRIANGLE_AUTO_CLICKER_BASE_COST,
        SQUARE_CLICK_REWARD, TRIANGLE_CLICK_REWARD
    )
    
    print("[OK] Constants loaded successfully")
    print(f"  Circle max points: {CIRCLE_MAX_POINTS:,}")
    print(f"  Square max points: {SQUARE_MAX_POINTS:,}")
    print(f"  Triangle max points: {TRIANGLE_MAX_POINTS:,}")
    print(f"  Square click reward: {SQUARE_CLICK_REWARD}")
    print(f"  Triangle click reward: {TRIANGLE_CLICK_REWARD}")

def test_upgrades():
    """Test the upgrade system"""
    from upgrades import UpgradeSystem
    
    print("\n[OK] Testing upgrade system...")
    upgrades = UpgradeSystem()
    
    # Test stage setting
    for stage in ["circle", "square", "triangle"]:
        upgrades.set_stage(stage)
        stats = upgrades.get_stats_text()
        print(f"  {stage.capitalize()} stage: Click power {stats['current_click_power']}, Click cost {stats['click_power_cost']}")

def test_shapes():
    """Test shape classes"""
    from shapes import CircleShape, SquareShape, TriangleShape
    
    print("\n[OK] Testing shape classes...")
    
    # Test circle
    circle = CircleShape(400, 300)
    print(f"  Circle created at ({circle.x}, {circle.y}) with radius {circle.radius}")
    
    # Test square
    square = SquareShape(400, 300)
    print(f"  Square created at ({square.x}, {square.y}) with size {square.size}")
    
    # Test triangle
    triangle = TriangleShape(400, 300)
    print(f"  Triangle created at ({triangle.x}, {triangle.y}) with side length {triangle.side_length}")

def test_game_initialization():
    """Test game initialization"""
    from game import ShapeClickerGame
    import pygame
    
    print("\n[OK] Testing game initialization...")
    pygame.init()
    
    game = ShapeClickerGame()
    print(f"  Game stage: {game.current_stage}")
    print(f"  Circle points: {game.circle_points}")
    print(f"  Square points: {game.square_points}")
    print(f"  Triangle points: {game.triangle_points}")
    
    pygame.quit()

if __name__ == "__main__":
    print("Shape Clicker Game - Feature Test")
    print("=" * 40)
    
    try:
        test_constants()
        test_upgrades()
        test_shapes()
        test_game_initialization()
        
        print("\n[SUCCESS] All tests passed! Game is ready to play.")
        print("\nTo start the game, run: python main.py")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        sys.exit(1)