import httpx
import logging
from utils.helpers import build_message_payload

logger = logging.getLogger("telegram-webhook")


async def handle_message(update: dict, bot_token: str):
    """
    Processes an incoming Telegram message update and replies accordingly.
    """

    if "message" not in update:
        logger.warning("⛔ No 'message' found in update.")
        return

    message = update["message"]
    chat = message.get("chat", {})
    text = message.get("text", "")

    chat_id = chat.get("id")
    if not chat_id:
        logger.error("❌ chat_id missing in update.")
        return

    if text.startswith("/start"):
        reply_text = "👋 Welcome! I'm your assistant bot."
    elif text.startswith("/help"):
        reply_text = (
            "ℹ️ Available commands:\n"
            "/start - Welcome message\n"
            "/help - Show this help info"
        )
    elif text:
        reply_text = f"🗣 You said: {text}"
    else:
        reply_text = "⚠️ I can only process text messages at the moment."

    payload = build_message_payload(chat_id, reply_text)

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json=payload
            )
            response.raise_for_status()
            logger.info(f"✅ Replied to chat_id: {chat_id}")
    except httpx.HTTPError as err:
        logger.error(f"❌ Failed to send message to {chat_id}: {err}")
        
