import json
import os
import aiofiles
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import config

class DataManager:
    def __init__(self):
        self.data_dir = config.DATA_DIR
        self.points_file = os.path.join(self.data_dir, "points.json")
        self.invites_file = os.path.join(self.data_dir, "invites.json")
        self.cooldowns_file = os.path.join(self.data_dir, "cooldowns.json")
        self.ensure_data_dir()
        self.load_data()

    def ensure_data_dir(self):
        """Ensure the data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load_data(self):
        """Load all data files"""
        self.points = self.load_json(self.points_file, {})
        self.invites = self.load_json(self.invites_file, {})
        self.cooldowns = self.load_json(self.cooldowns_file, {})

    def load_json(self, filepath: str, default: Dict) -> Dict:
        """Load JSON file with error handling"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return default

    async def save_json(self, filepath: str, data: Dict):
        """Save data to JSON file asynchronously"""
        try:
            async with aiofiles.open(filepath, 'w') as f:
                await f.write(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Error saving to {filepath}: {e}")

    # Point System Methods
    def get_points(self, user_id: int) -> int:
        """Get user's point balance"""
        return self.points.get(str(user_id), 0)

    async def add_points(self, user_id: int, points: int = 1):
        """Add points to user"""
        user_id_str = str(user_id)
        current_points = self.points.get(user_id_str, 0)
        self.points[user_id_str] = current_points + points
        await self.save_json(self.points_file, self.points)

    # Invite Tracking Methods
    def get_invite_count(self, user_id: int) -> int:
        """Get user's invite count"""
        user_id_str = str(user_id)
        count = self.invites.get(user_id_str, 0)
        print(f"Getting invite count for {user_id_str}: {count}")
        print(f"Current invites data: {self.invites}")
        return count

    async def add_invite(self, inviter_id: int, invitee_id: int):
        """Record an invite"""
        inviter_id_str = str(inviter_id)
        invitee_id_str = str(invitee_id)
        
        # Increment inviter's count
        current_invites = self.invites.get(inviter_id_str, 0)
        self.invites[inviter_id_str] = current_invites + 1
        
        print(f"Adding invite: inviter={inviter_id_str}, invitee={invitee_id_str}")
        print(f"Current invites data: {self.invites}")
        
        # Store invite relationship
        if 'relationships' not in self.invites:
            self.invites['relationships'] = {}
        self.invites['relationships'][invitee_id_str] = inviter_id_str
        
        await self.save_json(self.invites_file, self.invites)

    def get_inviter(self, user_id: int) -> Optional[int]:
        """Get who invited a user"""
        relationships = self.invites.get('relationships', {})
        inviter_id_str = relationships.get(str(user_id))
        return int(inviter_id_str) if inviter_id_str else None

    # Cooldown Methods
    def is_on_cooldown(self, user_id: int) -> bool:
        """Check if user is on vouch cooldown"""
        user_id_str = str(user_id)
        if user_id_str not in self.cooldowns:
            return False
        
        last_vouch = datetime.fromisoformat(self.cooldowns[user_id_str])
        cooldown_duration = timedelta(hours=config.VOUCH_COOLDOWN_HOURS)
        return datetime.now() - last_vouch < cooldown_duration

    async def set_cooldown(self, user_id: int):
        """Set vouch cooldown for user"""
        user_id_str = str(user_id)
        self.cooldowns[user_id_str] = datetime.now().isoformat()
        await self.save_json(self.cooldowns_file, self.cooldowns)

    def get_cooldown_remaining(self, user_id: int) -> Optional[timedelta]:
        """Get remaining cooldown time"""
        user_id_str = str(user_id)
        if user_id_str not in self.cooldowns:
            return None
        
        last_vouch = datetime.fromisoformat(self.cooldowns[user_id_str])
        cooldown_duration = timedelta(hours=config.VOUCH_COOLDOWN_HOURS)
        remaining = cooldown_duration - (datetime.now() - last_vouch)
        return remaining if remaining.total_seconds() > 0 else None

    # Leaderboard Methods
    def get_points_leaderboard(self, limit: int = 10) -> list:
        """Get top users by points"""
        sorted_users = sorted(self.points.items(), key=lambda x: x[1], reverse=True)
        return sorted_users[:limit]

    def get_invites_leaderboard(self, limit: int = 10) -> list:
        """Get top users by invites"""
        print(f"Getting invite leaderboard. Raw invites data: {self.invites}")
        # Filter out relationships from invite data
        invite_counts = {k: v for k, v in self.invites.items() if k != 'relationships'}
        print(f"Filtered invite counts: {invite_counts}")
        sorted_users = sorted(invite_counts.items(), key=lambda x: x[1], reverse=True)
        print(f"Sorted users: {sorted_users}")
        return sorted_users[:limit] 