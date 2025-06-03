import httpx
import logging
from utils.helpers import build_message_payload

logger = logging.getLogger("telegram-webhook")


async def handle_message(update: dict, bot_token: str):
    if "message" not in update:
        logger.warning("⛔ No 'message' found in update.")
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
          
