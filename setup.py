#!/usr/bin/env python3
"""
Setup script for Bob's Discount Shack Discord Bot
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    if os.path.exists(".env"):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists("env_example.txt"):
        try:
            with open("env_example.txt", "r") as f:
                content = f.read()
            
            with open(".env", "w") as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your bot token and channel IDs")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["data", "assets"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def check_configuration():
    """Check if configuration is complete"""
    print("\n🔧 Configuration Checklist:")
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ .env file exists")
        
        # Check for required variables
        with open(".env", "r") as f:
            content = f.read()
        
        required_vars = ["DISCORD_TOKEN", "GUILD_ID", "VOUCH_CHANNEL_ID", "ORDER_CHANNEL_IDS", "SUPPORT_CHANNEL_ID", "ADMIN_ROLE_ID"]
        for var in required_vars:
            if var in content and not content.split(var + "=")[1].split("\n")[0].startswith("your_"):
                print(f"✅ {var} is configured")
            else:
                print(f"⚠️  {var} needs to be configured")
    else:
        print("❌ .env file not found")
    
    # Check watermark
    if os.path.exists("assets/watermark.png"):
        print("✅ Watermark file exists")
    else:
        print("⚠️  Watermark file will be created automatically on first run")

def main():
    """Main setup function"""
    print("🤖 Bob's Discount Shack Discord Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check configuration
    check_configuration()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your bot token and channel IDs")
    print("2. Create your Discord bot and get the token")
    print("3. Set up your Discord server channels")
    print("4. Run: python main.py")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main() 