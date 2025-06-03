from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging
from app.config import settings
from app.handlers.message_handler import handle_message
from app.database import database

load_dotenv()

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("telegram-webhook")

@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info("Database connected")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info("Database disconnected")

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Webhook server is live."}

@app.post("/")
async def webhook_handler(request: Request):
    try:
        update = await request.json()
        logger.info(f"📩 Update received: {update}")

        await handle_message(update, settings.BOT_TOKEN)
        return JSONResponse(content={"ok": True})

    except Exception as e:
        logger.exception("❌ Error processing update")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
