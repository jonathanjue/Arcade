import pygame
from target import Target
from constants import TARGET_INITIAL_SPEED, SPEED_INCREASE_PERCENTAGE, MAX_SPEED

def test_difficulty_progression():
    """Test the difficulty progression system"""
    print("Testing difficulty progression...")

    # Create a target
    target = Target()

    # Test initial speed
    initial_speed = target.get_speed()
    print(f"Initial speed: {initial_speed}")
    assert initial_speed == TARGET_INITIAL_SPEED, f"Expected {TARGET_INITIAL_SPEED}, got {initial_speed}"

    # Test speed increase after multiple collisions
    for i in range(1, 10):
        # Simulate collision by calling respawn (which increases speed)
        target.respawn()

        current_speed = target.get_speed()
        print(f"Collision {i}: Speed = {current_speed:.2f}")

        # Verify speed doesn't exceed maximum
        assert current_speed <= MAX_SPEED, f"Speed {current_speed} exceeded maximum {MAX_SPEED}"

        # Verify speed increases (unless already at max)
        if i == 1:
            expected_min = initial_speed * (1 + SPEED_INCREASE_PERCENTAGE)
            assert current_speed >= expected_min, f"Speed increase too small: {current_speed} < {expected_min}"

    # Test that speed caps at maximum
    while target.get_speed() < MAX_SPEED:
        target.respawn()

    final_speed = target.get_speed()
    print(f"Final speed after capping: {final_speed:.2f}")
    assert final_speed == MAX_SPEED, f"Expected speed to cap at {MAX_SPEED}, got {final_speed}"

    print("All difficulty progression tests passed!")

if __name__ == "__main__":
    test_difficulty_progression()
