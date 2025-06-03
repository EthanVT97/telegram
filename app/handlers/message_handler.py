import logging
import httpx
from app.database import database, users
from app.utils import build_message_payload

logger = logging.getLogger("telegram-webhook")

async def track_user(update: dict):
    if "message" not in update:
        return
    msg = update["message"]
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    if not chat_id:
        return

    query = users.select().where(users.c.chat_id == chat_id)
    user = await database.fetch_one(query)
    user_data = {
        "chat_id": chat_id,
        "first_name": msg.get("from", {}).get("first_name"),
        "last_name": msg.get("from", {}).get("last_name"),
        "username": msg.get("from", {}).get("username"),
        "language_code": msg.get("from", {}).get("language_code"),
    }

    if user:
        update_query = users.update().where(users.c.chat_id == chat_id).values(
            message_count=user["message_count"] + 1,
            **user_data,
            updated_at=sqlalchemy.func.now()
        )
        await database.execute(update_query)
    else:
        insert_query = users.insert().values(
            **user_data,
            message_count=1,
        )
        await database.execute(insert_query)
    logger.info(f"Tracked user {chat_id}")

async def handle_message(update: dict, bot_token: str):
    await track_user(update)
    
    if "message" not in update:
        logger.warning("⛔ No message field found")
        return
    
    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):
        reply_text = "👋 Welcome! I'm your assistant bot."
    elif text.startswith("/help"):
        reply_text = "ℹ️ Available commands:\n/start - Welcome\n/help - Help info"
    elif text:
        reply_text = f"🗣 You said: {text}"
    else:
        reply_text = "⚠️ I can only process text messages for now."

    payload = build_message_payload(chat_id, reply_text)

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json=payload
            )
            res.raise_for_status()
            logger.info(f"✅ Replied to chat {chat_id}")
        except httpx.HTTPError as err:
            logger.error(f"❌ Failed to send message: {err}")
            
