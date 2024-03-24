import sys

from fastapi import APIRouter, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from . import message_event, user_event

sys.path.append(".")

import config

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

line_app = APIRouter()

# 監聽來自line的POST請求，並丟給handler進行處理
@line_app.post("/callback")
async def callback(request: Request) -> str:
    """LINE Bot webhook callback

    Args:
        request (Request): Request Object.

    Raises:
        HTTPException: Invalid Signature Error

    Returns:
        str: OK
    """
    signature = request.headers["X-Line-Signature"] #加入回傳的header
    body = await request.body() #取得收到的訊息內容
    
    # handle webhook body
    try:
        handler.handle(body.decode(), signature) #綁定訊息回傳的相關資訊
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")
    return "OK"


@handler.add(FollowEvent)
def handle_follow(event) -> None:
    """Event - User follow LINE Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#follow-event
    """
    user_event.handle_follow(event=event)


@handler.add(UnfollowEvent)
def handle_unfollow(event) -> None:
    """Event - User ban LINE Bot

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#unfollow-event
    """
    user_event.handle_unfollow(event=event)


@handler.add(MessageEvent, message=(TextMessage))
def handle_message(event) -> None:
    """Event - User sent message

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    message_event.handle_message(event=event)
