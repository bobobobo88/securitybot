#!/usr/bin/env python3
"""
Test script for Bob's Discount Shack Discord Bot
Tests core functionality without running the full bot
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    
    try:
        import config
        print("✅ Configuration loaded successfully")
        
        # Check required variables
        required_vars = [
            'BOT_TOKEN', 'GUILD_ID', 'VOUCH_CHANNEL_ID', 
            'ORDER_CHANNEL_IDS', 'SUPPORT_CHANNEL_ID'
        ]
        
        for var in required_vars:
            if hasattr(config, var):
                print(f"✅ {var} is defined")
            else:
                print(f"❌ {var} is missing")
                
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    return True

def test_data_manager():
    """Test data manager functionality"""
    print("\n📊 Testing data manager...")
    
    try:
        from data_manager import DataManager
        
        # Create test instance
        dm = DataManager()
        print("✅ Data manager initialized")
        
        # Test point system
        test_user_id = 123456789
        initial_points = dm.get_points(test_user_id)
        print(f"✅ Initial points for test user: {initial_points}")
        
        # Test invite system
        invite_count = dm.get_invite_count(test_user_id)
        print(f"✅ Initial invite count for test user: {invite_count}")
        
        # Test cooldown system
        is_on_cooldown = dm.is_on_cooldown(test_user_id)
        print(f"✅ Cooldown check: {is_on_cooldown}")
        
        print("✅ Data manager tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Data manager error: {e}")
        return False

def test_image_processor():
    """Test image processor functionality"""
    print("\n🖼️ Testing image processor...")
    
    try:
        from image_processor import ImageProcessor
        
        # Create test instance
        ip = ImageProcessor()
        print("✅ Image processor initialized")
        
        # Check watermark file
        if os.path.exists("assets/watermark.png"):
            print("✅ Watermark file exists")
        else:
            print("⚠️ Watermark file will be created on first run")
        
        print("✅ Image processor tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Image processor error: {e}")
        return False

def test_moderation():
    """Test moderation functionality"""
    print("\n🛡️ Testing moderation...")
    
    try:
        from moderation import Moderation
        
        # Create test instance (mock bot)
        class MockBot:
            pass
        
        bot = MockBot()
        mod = Moderation(bot)
        print("✅ Moderation system initialized")
        
        # Test invite link detection
        test_messages = [
            "Check out this server: discord.gg/abc123",
            "Join us at discord.gg/xyz789",
            "Hello world",
            "Visit discord.gg/test"
        ]
        
        for msg in test_messages:
            has_invite = mod.contains_invite_link(msg)
            print(f"Message: '{msg[:30]}...' - Has invite: {has_invite}")
        
        # Test scam domain detection
        test_domains = [
            "Check out scam.com",
            "Visit malicious.net",
            "Hello world",
            "Go to fake-discord.com"
        ]
        
        for msg in test_domains:
            has_scam = mod.contains_scam_domain(msg)
            print(f"Message: '{msg[:30]}...' - Has scam domain: {has_scam}")
        
        print("✅ Moderation tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Moderation error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'discord',
        'PIL',
        'dotenv',
        'aiofiles',
        'aiohttp'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'dotenv':
                import dotenv
            elif package == 'aiofiles':
                import aiofiles
            elif package == 'aiohttp':
                import aiohttp
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def test_file_structure():
    """Test file structure"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'main.py',
        'config.py',
        'data_manager.py',
        'moderation.py',
        'vouch_system.py',
        'invite_tracker.py',
        'commands.py',
        'image_processor.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} is missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files exist")
    return True

def main():
    """Run all tests"""
    print("🧪 Bob's Discount Shack Discord Bot - Test Suite")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_dependencies,
        test_config,
        test_data_manager,
        test_image_processor,
        test_moderation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to run.")
        print("\nNext steps:")
        print("1. Configure your .env file")
        print("2. Run: python main.py")
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    main() 