import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан")

# создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def download_tiktok(url: str) -> str | None:
    api_url = "https://www.tikwm.com/api/"
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data={"url": url}) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("data") and "play" in data["data"]:
                    play_url = data["data"]["play"]
                    if play_url.startswith("//"):
                        return "https:" + play_url
                    elif play_url.startswith("http"):
                        return play_url
    return None

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("привет! пришли мне ссылку на тикток, и я скачаю видео.")

@dp.message(F.text.contains("tiktok.com"))
async def tiktok_handler(message: Message):
    url = message.text.strip()
    await message.answer("почекай, ща скачаю...")
    video_url = await download_tiktok(url)
    if not video_url:
        await message.answer("не получилось. Перепроверь ссылку.")
        return
    await message.answer_video(video_url, caption="тримай своё видео")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
