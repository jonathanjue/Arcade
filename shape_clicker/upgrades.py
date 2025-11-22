"""Upgrade system for Shape Clicker"""

from constants import *


class UpgradeSystem:
    """Manages upgrades for the game with stage-specific scaling"""
    
    def __init__(self):
        # Upgrade levels
        self.click_power_level = 0
        self.auto_clicker_level = 0
        
        # Current upgrade costs (will be set based on stage)
        self.click_power_cost = CIRCLE_CLICK_POWER_BASE_COST
        self.auto_clicker_cost = CIRCLE_AUTO_CLICKER_BASE_COST
        
        # Stage-specific settings
        self.current_stage = "circle"
        self.base_click_power = 1  # Base points per click
        self.base_auto_clicker = 0  # Base points per second
        
        # Achievement tracking
        self.used_click_power = False
        self.used_auto_clicker = False
        self.used_manual_clicking = False  # Track if player clicked shapes manually
        self.stage_multiplier = 1.0  # Tracks progression multiplier
        self.multiplier_applied_stages = 0  # Track how many stages got multiplier
    
    def set_stage(self, stage_name):
        """Set the current stage and update costs accordingly"""
        self.current_stage = stage_name
        
        if stage_name == "circle":
            self.click_power_cost = CIRCLE_CLICK_POWER_BASE_COST
            self.auto_clicker_cost = CIRCLE_AUTO_CLICKER_BASE_COST
            self.base_click_power = 1
            self.base_auto_clicker = 0
        elif stage_name == "square":
            self.click_power_cost = SQUARE_CLICK_POWER_BASE_COST
            self.auto_clicker_cost = SQUARE_AUTO_CLICKER_BASE_COST
            self.base_click_power = SQUARE_CLICK_REWARD  # 5 points per click
            self.base_auto_clicker = 0
        elif stage_name == "triangle":
            self.click_power_cost = TRIANGLE_CLICK_POWER_BASE_COST
            self.auto_clicker_cost = TRIANGLE_AUTO_CLICKER_BASE_COST
            self.base_click_power = TRIANGLE_CLICK_REWARD  # 25 points per click
            self.base_auto_clicker = 0
    
    def get_click_power(self):
        """Get current click power (points per click)"""
        return (self.base_click_power + self.click_power_level) * self.stage_multiplier
    
    def get_points_per_second(self):
        """Get current auto clicker points per second"""
        # Auto clicker uses the current stage's click power as base, multiplied by stage bonus
        if self.current_stage == "triangle":
            base_points = self.base_click_power * self.auto_clicker_level
        else:
            # For circle and square stages, auto clicker gives 1 point per level per second
            base_points = self.auto_clicker_level
        
        return base_points * self.stage_multiplier
    
    def can_afford_click_power(self, current_points):
        """Check if player can afford click power upgrade"""
        return current_points >= self.click_power_cost
    
    def can_afford_auto_clicker(self, current_points):
        """Check if player can afford auto clicker upgrade"""
        return current_points >= self.auto_clicker_cost
    
    def buy_click_power(self, current_points):
        """Buy click power upgrade, return points spent and new points"""
        if self.can_afford_click_power(current_points):
            current_points -= self.click_power_cost
            self.click_power_level += 1
            self.click_power_cost = int(self.click_power_cost * CLICK_POWER_COST_MULTIPLIER)
            return True, current_points
        return False, current_points
    
    def buy_auto_clicker(self, current_points):
        """Buy auto clicker upgrade, return success and new points"""
        if self.can_afford_auto_clicker(current_points):
            current_points -= self.auto_clicker_cost
            self.auto_clicker_level += 1
            self.auto_clicker_cost = int(self.auto_clicker_cost * AUTO_CLICKER_COST_MULTIPLIER)
            return True, current_points
        return False, current_points
    
    def reset(self):
        """Reset all upgrades but keep current stage settings"""
        self.click_power_level = 0
        self.auto_clicker_level = 0
        # Reset costs based on current stage
        self.set_stage(self.current_stage)
    
    def advance_stage(self, had_auto_clicker):
        """Advance to next stage and apply multiplier if applicable"""
        if had_auto_clicker:
            self.stage_multiplier *= ACHIEVEMENT_MULTIPLIER
            self.multiplier_applied_stages += 1
            return True  # Multiplier applied
        return False  # No multiplier
    
    def check_achievement_criteria(self):
        """Check if achievements were earned during gameplay"""
        return {
            'pure_clicker': not self.used_auto_clicker and self.used_click_power,
            'auto_master': not self.used_click_power and self.used_auto_clicker,
            'robot': not self.used_manual_clicking and self.used_auto_clicker  # No clicking, only auto clickers
        }
    
    def record_upgrade_usage(self, upgrade_type):
        """Record when an upgrade type is used"""
        if upgrade_type == 'click_power':
            self.used_click_power = True
        elif upgrade_type == 'auto_clicker':
            self.used_auto_clicker = True
    
    def get_multiplier_info(self):
        """Get current multiplier information"""
        return {
            'current_multiplier': self.stage_multiplier,
            'stages_with_multiplier': self.multiplier_applied_stages,
            'base_click_power': self.base_click_power,
            'multiplied_click_power': self.base_click_power * self.stage_multiplier,
            'base_points_per_second': self.base_auto_clicker * self.stage_multiplier
        }
    
    def get_stats_text(self):
        """Get formatted text for upgrade stats"""
        click_power = self.get_click_power()
        points_per_sec = self.get_points_per_second()
        
        return {
            'click_power_level': self.click_power_level,
            'auto_clicker_level': self.auto_clicker_level,
            'current_click_power': click_power,
            'current_points_per_second': points_per_sec,
            'click_power_cost': self.click_power_cost,
            'auto_clicker_cost': self.auto_clicker_cost,
            'stage': self.current_stage
        }