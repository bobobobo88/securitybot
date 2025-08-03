#!/usr/bin/env python3
"""
Simple script to set up .env file from template
"""

import os
import shutil

def setup_env():
    """Set up .env file from template"""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return
    
    if os.path.exists('env_example.txt'):
        shutil.copy('env_example.txt', '.env')
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your actual values:")
        print("   - DISCORD_TOKEN")
        print("   - GUILD_ID") 
        print("   - VOUCH_CHANNEL_ID")
        print("   - ORDER_CHANNEL_IDS")
        print("   - SUPPORT_CHANNEL_ID")
        print("   - ADMIN_ROLE_ID")
        print("   - VERIFIED_ROLE_ID")
        print("   - MUTED_ROLE_ID")
    else:
        print("❌ env_example.txt not found")

if __name__ == "__main__":
    setup_env() 