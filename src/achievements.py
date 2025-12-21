"""
🏆 ForkMonkey Achievement System

Track milestones and unlock achievements as your monkey evolves.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path


# Achievement Definitions
ACHIEVEMENTS = {
    # Getting Started
    "first_hatch": {
        "icon": "🥚",
        "title": "First Hatch",
        "description": "Adopted your first monkey",
        "category": "milestone",
        "condition": lambda stats, dna: stats.get("created_at") is not None
    },
    
    # Evolution Streaks
    "week_streak": {
        "icon": "🔥",
        "title": "Week Warrior",
        "description": "7-day evolution streak",
        "category": "streak",
        "condition": lambda stats, dna: stats.get("age_days", 0) >= 7
    },
    "month_keeper": {
        "icon": "💎",
        "title": "Diamond Hands",
        "description": "Kept your monkey for 30 days",
        "category": "streak",
        "condition": lambda stats, dna: stats.get("age_days", 0) >= 30
    },
    "century_club": {
        "icon": "💯",
        "title": "Century Club",
        "description": "100 days with your monkey",
        "category": "streak",
        "condition": lambda stats, dna: stats.get("age_days", 0) >= 100
    },
    
    # Rarity Achievements
    "rare_trait": {
        "icon": "⭐",
        "title": "Lucky Find",
        "description": "Obtained a rare trait",
        "category": "rarity",
        "condition": lambda stats, dna: _has_rarity(dna, "rare")
    },
    "legendary": {
        "icon": "🦄",
        "title": "Legendary",
        "description": "Obtained a legendary trait",
        "category": "rarity",
        "condition": lambda stats, dna: _has_rarity(dna, "legendary")
    },
    "high_rarity": {
        "icon": "🌟",
        "title": "Rare Breed",
        "description": "Rarity score above 50",
        "category": "rarity",
        "condition": lambda stats, dna: stats.get("rarity_score", 0) >= 50
    },
    "elite_rarity": {
        "icon": "👑",
        "title": "Elite",
        "description": "Rarity score above 75",
        "category": "rarity",
        "condition": lambda stats, dna: stats.get("rarity_score", 0) >= 75
    },
    
    # Mutation Achievements
    "first_mutation": {
        "icon": "🧬",
        "title": "First Change",
        "description": "First AI mutation",
        "category": "mutation",
        "condition": lambda stats, dna: stats.get("total_mutations", 0) >= 1
    },
    "mutant": {
        "icon": "🔬",
        "title": "Mutant",
        "description": "10 total mutations",
        "category": "mutation",
        "condition": lambda stats, dna: stats.get("total_mutations", 0) >= 10
    },
    "evolved": {
        "icon": "🦋",
        "title": "Fully Evolved",
        "description": "50 total mutations",
        "category": "mutation",
        "condition": lambda stats, dna: stats.get("total_mutations", 0) >= 50
    },
    
    # Social Achievements  
    "parent": {
        "icon": "👶",
        "title": "Proud Parent",
        "description": "Someone forked your monkey",
        "category": "social",
        "condition": lambda stats, dna: stats.get("children_count", 0) >= 1
    },
    "dynasty": {
        "icon": "👑",
        "title": "Dynasty Founder",
        "description": "5+ descendants from your monkey",
        "category": "social",
        "condition": lambda stats, dna: stats.get("children_count", 0) >= 5
    },
    "influencer": {
        "icon": "📣",
        "title": "Monkey Influencer",
        "description": "10+ descendants from your monkey",
        "category": "social",
        "condition": lambda stats, dna: stats.get("children_count", 0) >= 10
    },
    
    # Leaderboard
    "top_100": {
        "icon": "📊",
        "title": "Top 100",
        "description": "Reached top 100 in rarity leaderboard",
        "category": "leaderboard",
        "condition": lambda stats, dna: stats.get("leaderboard_rank", 999) <= 100
    },
    "top_10": {
        "icon": "🏆",
        "title": "Top 10",
        "description": "Reached top 10 in rarity leaderboard",
        "category": "leaderboard",
        "condition": lambda stats, dna: stats.get("leaderboard_rank", 999) <= 10
    },
    "champion": {
        "icon": "🥇",
        "title": "Champion",
        "description": "Reached #1 in rarity leaderboard",
        "category": "leaderboard",
        "condition": lambda stats, dna: stats.get("leaderboard_rank", 999) == 1
    },
    
    # Special Traits
    "accessorized": {
        "icon": "🎩",
        "title": "Accessorized",
        "description": "Has an accessory equipped",
        "category": "traits",
        "condition": lambda stats, dna: dna.get("accessory", "None") != "None"
    },
    "patterned": {
        "icon": "🎨",
        "title": "Patterned",
        "description": "Has a special pattern",
        "category": "traits",
        "condition": lambda stats, dna: dna.get("pattern", "None") != "None"
    },
    "special_one": {
        "icon": "✨",
        "title": "The Special One",
        "description": "Has a special trait",
        "category": "traits",
        "condition": lambda stats, dna: dna.get("special", "None") != "None"
    },
    
    # Generation
    "gen_2": {
        "icon": "2️⃣",
        "title": "Second Gen",
        "description": "A 2nd generation monkey",
        "category": "generation",
        "condition": lambda stats, dna: stats.get("generation", 1) >= 2
    },
    "gen_5": {
        "icon": "5️⃣",
        "title": "Fifth Gen",
        "description": "A 5th generation monkey",
        "category": "generation",
        "condition": lambda stats, dna: stats.get("generation", 1) >= 5
    },
}


def _has_rarity(dna: Dict, target_rarity: str) -> bool:
    """Check if DNA has any trait with the target rarity."""
    from genetics import TRAITS
    
    for trait_name, trait_value in dna.items():
        if trait_name in TRAITS:
            trait_options = TRAITS[trait_name]
            for option in trait_options:
                if option.get("name") == trait_value:
                    if option.get("rarity", "common").lower() == target_rarity.lower():
                        return True
    return False


def check_achievements(stats: Dict[str, Any], dna: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check which achievements have been unlocked.
    
    Args:
        stats: Monkey statistics dictionary
        dna: Monkey DNA dictionary
        
    Returns:
        List of unlocked achievement dictionaries
    """
    unlocked = []
    
    for key, achievement in ACHIEVEMENTS.items():
        try:
            if achievement["condition"](stats, dna):
                unlocked.append({
                    "key": key,
                    "icon": achievement["icon"],
                    "title": achievement["title"],
                    "description": achievement["description"],
                    "category": achievement["category"]
                })
        except Exception:
            # Skip achievements that fail to evaluate
            pass
    
    return unlocked


def get_achievement_progress(stats: Dict[str, Any], dna: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get progress towards all achievements.
    
    Returns a dictionary with unlocked achievements and total counts.
    """
    unlocked = check_achievements(stats, dna)
    
    # Group by category
    by_category = {}
    for achievement in unlocked:
        category = achievement["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(achievement)
    
    return {
        "unlocked": unlocked,
        "unlocked_count": len(unlocked),
        "total_count": len(ACHIEVEMENTS),
        "by_category": by_category,
        "percentage": round((len(unlocked) / len(ACHIEVEMENTS)) * 100, 1)
    }


def save_achievements(achievements: List[Dict], path: str = "monkey_data/achievements.json"):
    """Save unlocked achievements to file."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump({
            "unlocked": achievements,
            "updated_at": datetime.utcnow().isoformat()
        }, f, indent=2)


def load_achievements(path: str = "monkey_data/achievements.json") -> List[Dict]:
    """Load achievements from file."""
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data.get("unlocked", [])
    except FileNotFoundError:
        return []


def format_achievements_display(achievements: List[Dict]) -> str:
    """Format achievements for display in README or terminal."""
    if not achievements:
        return "No achievements unlocked yet! Keep evolving! 🐵"
    
    lines = ["### 🏆 Achievements", ""]
    
    # Group by category
    by_category = {}
    for a in achievements:
        cat = a.get("category", "other")
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(a)
    
    for category, items in by_category.items():
        icons = " ".join([a["icon"] for a in items])
        lines.append(f"**{category.title()}**: {icons}")
    
    lines.append("")
    lines.append(f"*{len(achievements)}/{len(ACHIEVEMENTS)} unlocked*")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample data
    sample_stats = {
        "age_days": 15,
        "rarity_score": 45,
        "generation": 2,
        "total_mutations": 12,
        "children_count": 2,
        "created_at": "2024-01-01"
    }
    
    sample_dna = {
        "body_color": "Purple",
        "accessory": "Crown",
        "pattern": "Stars",
        "special": "None"
    }
    
    progress = get_achievement_progress(sample_stats, sample_dna)
    print(f"🏆 Achievements: {progress['unlocked_count']}/{progress['total_count']} ({progress['percentage']}%)")
    print()
    for achievement in progress['unlocked']:
        print(f"  {achievement['icon']} {achievement['title']}: {achievement['description']}")

