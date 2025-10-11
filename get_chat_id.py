#!/usr/bin/env python3
"""
Get your Telegram Chat ID
Run this after sending a message to your bot
"""

import asyncio
from telegram import Bot
from config import Settings

async def get_chat_id():
    print("="*60)
    print("🔍 FINDING YOUR CHAT ID")
    print("="*60)
    print()
    
    bot = Bot(token=Settings.TELEGRAM_BOT_TOKEN)
    
    print("Checking for recent messages...")
    print()
    
    try:
        # Get updates
        updates = await bot.get_updates()
        
        if not updates:
            print("❌ No messages found!")
            print()
            print("To get your Chat ID:")
            print("1. Open Telegram")
            print("2. Search for your bot")
            print("3. Send /start or any message to it")
            print("4. Run this script again")
            print()
            print("Or use @userinfobot:")
            print("1. Search for @userinfobot in Telegram")
            print("2. Send any message")
            print("3. It will reply with your Chat ID")
            return
        
        print("✅ Found messages!")
        print()
        
        # Show all chat IDs found
        chat_ids = set()
        for update in updates:
            if update.message:
                chat_id = update.message.chat.id
                username = update.message.from_user.username or "No username"
                first_name = update.message.from_user.first_name or ""
                
                chat_ids.add(chat_id)
                
                print(f"Chat ID: {chat_id}")
                print(f"Name: {first_name}")
                print(f"Username: @{username}")
                print(f"Message: {update.message.text}")
                print("-"*60)
        
        if chat_ids:
            print()
            print("💡 Add this to your .env file:")
            print()
            for chat_id in chat_ids:
                print(f"TELEGRAM_CHAT_ID={chat_id}")
            print()
            
            # Test sending a message
            test_chat_id = list(chat_ids)[0]
            print(f"Testing notification to Chat ID {test_chat_id}...")
            
            try:
                await bot.send_message(
                    chat_id=test_chat_id,
                    text="🎉 Telegram notifications configured!\n\nYour trading bot can now send you alerts."
                )
                print("✅ Test message sent successfully!")
            except Exception as e:
                print(f"⚠️  Could not send test message: {e}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Make sure:")
        print("- Bot token is correct in .env")
        print("- You've sent a message to the bot")

if __name__ == '__main__':
    asyncio.run(get_chat_id())
