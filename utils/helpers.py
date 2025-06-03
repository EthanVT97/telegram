def build_message_payload(chat_id: int, text: str) -> dict:
    return {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
  
