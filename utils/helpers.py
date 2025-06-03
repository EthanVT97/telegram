from typing import List, Dict, Optional, Union


def build_message_payload(
    chat_id: int,
    text: Optional[str] = None,
    parse_mode: str = "HTML",
    disable_web_page_preview: bool = True,
    reply_markup: Optional[Dict] = None,
    photo_url: Optional[str] = None,
    document_url: Optional[str] = None,
    video_url: Optional[str] = None,
    audio_url: Optional[str] = None,
    caption: Optional[str] = None
) -> Dict[str, Union[str, int, dict]]:
    """
    Dynamically builds payload for different message types:
    - sendMessage
    - sendPhoto
    - sendDocument
    - sendVideo
    - sendAudio
    Based on which media URL is supplied.
    """

    payload = {
        "chat_id": chat_id,
        "parse_mode": parse_mode,
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    if photo_url:
        payload["photo"] = photo_url
        payload["caption"] = caption or text or ""
        return payload  # Use with sendPhoto

    if document_url:
        payload["document"] = document_url
        payload["caption"] = caption or text or ""
        return payload  # Use with sendDocument

    if video_url:
        payload["video"] = video_url
        payload["caption"] = caption or text or ""
        return payload  # Use with sendVideo

    if audio_url:
        payload["audio"] = audio_url
        payload["caption"] = caption or text or ""
        return payload  # Use with sendAudio

    # Default: plain text message
    payload["text"] = text or ""
    payload["disable_web_page_preview"] = disable_web_page_preview
    return payload  # Use with sendMessage


def build_inline_keyboard(buttons: List[List[Dict[str, str]]]) -> Dict:
    """
    Builds an inline keyboard.
    Example:
    build_inline_keyboard([
        [{"text": "Google", "url": "https://google.com"}],
        [{"text": "Say Hi", "callback_data": "say_hi"}]
    ])
    """
    return {"inline_keyboard": buttons}


def build_reply_keyboard(
    buttons: List[List[str]],
    resize_keyboard: bool = True,
    one_time_keyboard: bool = False
) -> Dict:
    """
    Builds a reply keyboard (shows as buttons below input field).
    Example:
    build_reply_keyboard([
        ["Yes", "No"],
        ["Maybe"]
    ])
    """
    return {
        "keyboard": [[{"text": b} for b in row] for row in buttons],
        "resize_keyboard": resize_keyboard,
        "one_time_keyboard": one_time_keyboard
    }


def build_remove_keyboard() -> Dict:
    """
    Removes custom keyboard.
    """
    return {"remove_keyboard": True}


def get_api_endpoint(payload: Dict) -> str:
    """
    Determines the correct Telegram API endpoint based on payload content.
    """
    if "photo" in payload:
        return "sendPhoto"
    elif "document" in payload:
        return "sendDocument"
    elif "video" in payload:
        return "sendVideo"
    elif "audio" in payload:
        return "sendAudio"
    else:
        return "sendMessage"
        
