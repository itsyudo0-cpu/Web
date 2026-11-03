"""
CleanReader & Media Summarizer Bot - Entry Point (main.py)
==========================================================
Initializes the Pyrogram v2.x Client, Motor MongoDB indexes,
Telegraph Instant View account, and background tasks.
"""

import asyncio
import logging
from pyrogram import Client, idle
from pyrogram.enums import ParseMode
from config import Config
from database import db
from utils.extractor import extractor_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("CleanReaderBot")
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def main() -> None:
    Config.validate()

    # Initialize MongoDB indexes
    await db.initialize_indexes()

    # Initialize Telegraph account for Instant View publishing
    await extractor_service.init_telegraph()

    app = Client(
        name="cleanreader_bot_session",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN,
        plugins=dict(root="plugins"),
        parse_mode=ParseMode.HTML,
        workers=16,
    )

    logger.info("Starting CleanReader & Media Summarizer Bot...")
    await app.start()

    me = await app.get_me()
    Config.BOT_USERNAME = me.username or Config.BOT_USERNAME
    logger.info(
        "Bot online as @%s (ID: %s) | FSUB: %s | Log Channel: %s",
        me.username,
        me.id,
        Config.FSUB_CHANNEL_ID,
        Config.LOG_CHANNEL_ID,
    )

    await idle()
    logger.info("Shutting down CleanReader Bot...")
    await app.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped cleanly.")


import os
import asyncio
from aiohttp import web
from pyrogram import Client

# Dummy route taaki Render ko 200 OK mile
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render PORT environment variable provide karta hai (default 8080/10000)
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server started on port {port}")

# Bot start hone ke sath server ko run karein
async def main():
    # Pehle web server start karein taaki port open ho jaye
    await start_web_server()
    
    # Uske baad bot start karein
    await bot.start()
    print("Bot started successfully!")
    await asyncio.Event().wait()  # Keeps bot running

if __name__ == "__main__":
    asyncio.run(main())
