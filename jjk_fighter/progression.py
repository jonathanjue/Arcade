import json
import os

SAVE_PATH = os.path.join(os.path.dirname(__file__), "data", "save.json")

DEFAULT_SAVE = {
    "player_level": 1,
    "player_xp": 0,
    "cursed_points": 0,
    "unlocked_characters": ["yuji", "gojo", "sukuna", "megumi"],
    "unlocked_stages": ["shibuya"],
    "story_progress": 0,  # 0-12
    "completed_chapters": [],
    "achievements": [],
    "total_wins": 0,
    "total_losses": 0,
    "total_perfects": 0,
    "highest_combo": 0,
    "highest_survival_wave": 0,
    "character_wins": {},
    "character_usage": {},
    "settings": {
        "music_volume": 0.7,
        "sfx_volume": 0.8,
        "difficulty": "normal",
    }
}

ACHIEVEMENTS = {
    "first_blood": {"name": "First Blood", "desc": "Win your first fight", "icon": "1"},
    "perfect_round": {"name": "Perfect", "desc": "Win a round without taking damage", "icon": "P"},
    "combo_10": {"name": "Combo Master", "desc": "Reach a 10-hit combo", "icon": "10"},
    "domain_master": {"name": "Domain Expansion", "desc": "Use a Domain Expansion", "icon": "D"},
    "black_flash": {"name": "Black Flash", "desc": "Land a Black Flash", "icon": "BF"},
    "story_complete": {"name": "Cursed Journey", "desc": "Complete Story Mode", "icon": "S"},
    "all_chars": {"name": "Collector", "desc": "Unlock all characters", "icon": "A"},
    "survival_10": {"name": "Survivor", "desc": "Reach wave 10 in Survival", "icon": "W10"},
    "win_streak_10": {"name": "On Fire", "desc": "Win 10 fights in a row", "icon": "10W"},
    "sukuna_defeated": {"name": "King Slayer", "desc": "Defeat Sukuna in Story", "icon": "KS"},
}

class ProgressionSystem:
    def __init__(self):
        self.data = self.load()
        self.win_streak = 0

    def load(self):
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        if os.path.exists(SAVE_PATH):
            try:
                with open(SAVE_PATH, "r") as f:
                    data = json.load(f)
                # Merge with defaults for missing keys
                for key, val in DEFAULT_SAVE.items():
                    if key not in data:
                        data[key] = val
                return data
            except Exception:
                pass
        return dict(DEFAULT_SAVE)

    def save(self):
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with open(SAVE_PATH, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_cursed_points(self, amount):
        self.data["cursed_points"] += amount
        self.save()

    def spend_cursed_points(self, amount):
        if self.data["cursed_points"] >= amount:
            self.data["cursed_points"] -= amount
            self.save()
            return True
        return False

    def unlock_character(self, char_id):
        if char_id not in self.data["unlocked_characters"]:
            self.data["unlocked_characters"].append(char_id)
            self.save()
            return True
        return False

    def unlock_stage(self, stage_id):
        if stage_id not in self.data["unlocked_stages"]:
            self.data["unlocked_stages"].append(stage_id)
            self.save()
            return True
        return False

    def is_character_unlocked(self, char_id):
        return char_id in self.data["unlocked_characters"]

    def is_stage_unlocked(self, stage_id):
        return stage_id in self.data["unlocked_stages"]

    def complete_chapter(self, chapter_id):
        if chapter_id not in self.data["completed_chapters"]:
            self.data["completed_chapters"].append(chapter_id)
            self.data["story_progress"] = max(self.data["story_progress"], chapter_id)
            self.save()

    def record_win(self, char_id, is_perfect=False):
        self.data["total_wins"] += 1
        self.data["character_wins"][char_id] = self.data["character_wins"].get(char_id, 0) + 1
        self.data["character_usage"][char_id] = self.data["character_usage"].get(char_id, 0) + 1
        self.win_streak += 1
        if is_perfect:
            self.data["total_perfects"] += 1
            self.unlock_achievement("perfect_round")
        if self.data["total_wins"] == 1:
            self.unlock_achievement("first_blood")
        if self.win_streak >= 10:
            self.unlock_achievement("win_streak_10")
        # XP gain
        self.data["player_xp"] += 25
        if self.data["player_xp"] >= self.data["player_level"] * 100:
            self.data["player_xp"] -= self.data["player_level"] * 100
            self.data["player_level"] += 1
            self.data["cursed_points"] += 50
        self.save()

    def record_loss(self):
        self.data["total_losses"] += 1
        self.win_streak = 0
        self.data["player_xp"] += 10
        self.save()

    def record_combo(self, hits):
        if hits > self.data["highest_combo"]:
            self.data["highest_combo"] = hits
        if hits >= 10:
            self.unlock_achievement("combo_10")
        self.save()

    def record_domain(self):
        self.unlock_achievement("domain_master")

    def record_black_flash(self):
        self.unlock_achievement("black_flash")

    def record_survival_wave(self, wave):
        if wave > self.data["highest_survival_wave"]:
            self.data["highest_survival_wave"] = wave
        if wave >= 10:
            self.unlock_achievement("survival_10")
        self.save()

    def unlock_achievement(self, ach_id):
        if ach_id not in self.data["achievements"]:
            self.data["achievements"].append(ach_id)
            self.save()
            return ACHIEVEMENTS.get(ach_id)
        return None

    def get_achievements(self):
        return [(aid, ACHIEVEMENTS.get(aid, {})) for aid in self.data["achievements"]]

    def get_all_achievements(self):
        return ACHIEVEMENTS

    def check_story_complete(self):
        if len(self.data["completed_chapters"]) >= 12:
            self.unlock_achievement("story_complete")
            self.unlock_character("kenjaku")  # Secret unlock

    def check_all_chars(self):
        if len(self.data["unlocked_characters"]) >= 12:
            self.unlock_achievement("all_chars")
