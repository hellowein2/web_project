import asyncio
import os
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request
import httpx


app = FastAPI()

TOKEN = '7615818872:AAH4ws6ueyaRBtd4SImsvqPjWVcngIWE9Ao'


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id", "")
    text = message.get("text", "")

    if chat_id and text.lower() == "hello":
        await send_message(chat_id, "Привет! Нажмите кнопку ниже, чтобы открыть приложение.")
    elif chat_id:
        await send_web_app_button(chat_id)

    return {"ok": True}


async def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)


async def send_web_app_button(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "Откройте веб-приложение, нажав кнопку ниже.",
        "reply_markup": {
            "inline_keyboard": [[{
                "text": "Открыть приложение",
            }]]
        }
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
