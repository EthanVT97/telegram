from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import logging
from handlers.message_handler import handle_message

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN must be set in the environment variables.")

app = FastAPI()

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("telegram-webhook")


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Webhook server is live."}


@app.post("/")
async def webhook_handler(request: Request):
    try:
        update = await request.json()
        logger.info(f"📩 Update received: {update}")

        await handle_message(update, BOT_TOKEN)
        return JSONResponse(content={"ok": True})

    except Exception as e:
        logger.exception("❌ Error processing update")
        raise HTTPException(status_code=500, detail="Internal Server Error")
